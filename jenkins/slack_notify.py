import argparse
import os
import json
import requests


def send_slack_message(webhook_url, status, message):
    color = '#36a64f' if status == 'success' else '#ff0000' if status == 'failure' else '#ffaa00'
    payload = {
        'attachments': [
            {
                'color': color,
                'title': f'Deployment {status.upper()}',
                'text': message,
                'fields': [
                    {'title': 'Environment', 'value': os.environ.get('ENVIRONMENT', 'unknown'), 'short': True},
                    {'title': 'Team', 'value': os.environ.get('TEAM_NAME', 'unknown'), 'short': True},
                    {'title': 'Product', 'value': os.environ.get('PRODUCT', 'unknown'), 'short': True},
                    {'title': 'Team Lead', 'value': os.environ.get('TEAM_LEAD', 'unknown'), 'short': True},
                    {'title': 'Team VIP', 'value': os.environ.get('TEAM_VIP', 'unknown'), 'short': True},
                    {'title': 'Budget ID', 'value': os.environ.get('TEAM_BUDGET_ID', 'unknown'), 'short': True},
                ],
            }
        ]
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    response.raise_for_status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('status', choices=['success', 'failure', 'warning'])
    parser.add_argument('message', help='Message to send to Slack')
    args = parser.parse_args()

    webhook_url = os.environ.get('SLACK_WEBHOOK')
    if not webhook_url:
        raise SystemExit('SLACK_WEBHOOK environment variable is required')

    send_slack_message(webhook_url, args.status, args.message)
