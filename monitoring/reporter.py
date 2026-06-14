import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from collector_utils import post_json, render_plot_base64

logger = logging.getLogger(__name__)


def render_report(template_name: str, context: dict) -> str:
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(templates_path), autoescape=True)
    template = env.get_template(template_name)
    return template.render(context)


def build_email(subject: str, body: str, from_address: str, to_addresses: list) -> MIMEMultipart:
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = from_address
    message['To'] = ', '.join(to_addresses)
    message.attach(MIMEText(body, 'html'))
    return message


def send_email(smtp_host: str, smtp_port: int, from_address: str, to_addresses: list, message: MIMEMultipart, username: str = None, password: str = None):
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            if username and password:
                smtp.login(username, password)
            smtp.sendmail(from_address, to_addresses, message.as_string())
            logger.info('Sent report email to %s', to_addresses)
    except Exception as exc:
        logger.error('Failed to send email: %s', exc)


def post_teams_webhook(webhook_url: str, title: str, text: str):
    if not webhook_url:
        logger.warning('Teams webhook URL is not configured.')
        return {}
    payload = {
        'text': f"**{title}**\n{text}"
    }
    return post_json(webhook_url, payload=payload)


def send_reports(config: dict, environment: str, health_summary: dict, waste_df, cloud_waste: dict):
    env_cfg = config['environments'][environment]
    report_context = {
        'environment': env_cfg['label'],
        'generated_at': health_summary['generated_at'],
        'cluster_count': health_summary['cluster_count'],
        'critical_alerts': health_summary['critical_alerts'].to_dict(orient='records') if not health_summary['critical_alerts'].empty else [],
        'restart_summary': health_summary['restarts'].to_dict(orient='records'),
        'red_alerts': health_summary['red_alerts'].to_dict(orient='records') if not health_summary['red_alerts'].empty else [],
        'waste_summary': waste_df.to_dict(orient='records') if not waste_df.empty else [],
        'cloud_waste': cloud_waste,
    }

    monitoring_html = render_report('monitoring_report.html', report_context)
    waste_html = render_report('waste_report.html', report_context)

    monitoring_message = build_email(
        f"{config['report']['subject_prefix']} - {env_cfg['label']} Monitoring",
        monitoring_html,
        config['report']['from_address'],
        env_cfg['outlook']['monitoring_to'],
    )
    waste_message = build_email(
        f"{config['report']['subject_prefix']} - {env_cfg['label']} Waste Report",
        waste_html,
        config['report']['from_address'],
        env_cfg['outlook']['waste_to'],
    )

    send_email(
        smtp_host=os.environ.get('SMTP_HOST', config['report'].get('smtp_host', 'smtp.office365.com')),
        smtp_port=int(os.environ.get('SMTP_PORT', config['report'].get('smtp_port', 587))),
        from_address=config['report']['from_address'],
        to_addresses=env_cfg['outlook']['monitoring_to'],
        message=monitoring_message,
        username=config['report'].get('smtp_username'),
        password=config['report'].get('smtp_password'),
    )

    send_email(
        smtp_host=os.environ.get('SMTP_HOST', config['report'].get('smtp_host', 'smtp.office365.com')),
        smtp_port=int(os.environ.get('SMTP_PORT', config['report'].get('smtp_port', 587))),
        from_address=config['report']['from_address'],
        to_addresses=env_cfg['outlook']['waste_to'],
        message=waste_message,
        username=config['report'].get('smtp_username'),
        password=config['report'].get('smtp_password'),
    )

    post_teams_webhook(env_cfg['teams']['monitoring_webhook'], f"{env_cfg['label']} Monitoring Report", f"Monitoring report for {env_cfg['label']} has been sent to email.")
    post_teams_webhook(env_cfg['teams']['waste_webhook'], f"{env_cfg['label']} Waste Report", f"Waste report for {env_cfg['label']} has been sent to email.")
