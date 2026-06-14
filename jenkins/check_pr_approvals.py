import argparse
import os
import re
import requests


def get_pr_approvals(repo_full_name, pr_number, github_token):
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/reviews"
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github+json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    reviews = response.json()

    approvers = set()
    for review in reviews:
        if review.get('state') == 'APPROVED':
            approvers.add(review.get('user', {}).get('login'))
    return len(approvers)


def parse_pr_url(pr_url):
    pattern = r"https?://github\.com/(?P<repo>[^/]+/[^/]+)/pull/(?P<pr>\d+)"
    match = re.search(pattern, pr_url)
    if not match:
        raise ValueError('PR URL must be a GitHub pull request URL.')
    return match.group('repo'), match.group('pr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr-url', help='GitHub pull request URL')
    parser.add_argument('--repo', help='GitHub repo full name owner/repo')
    parser.add_argument('--pr', help='Pull request number')
    args = parser.parse_args()

    if args.pr_url:
        repo_full_name, pr_number = parse_pr_url(args.pr_url)
    elif args.repo and args.pr:
        repo_full_name, pr_number = args.repo, args.pr
    else:
        raise SystemExit('Either --pr-url or both --repo and --pr must be provided.')

    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise SystemExit('GITHUB_TOKEN environment variable is required')

    approvals = get_pr_approvals(repo_full_name, pr_number, token)
    print(approvals)
