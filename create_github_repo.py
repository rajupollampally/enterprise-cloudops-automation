import os
import subprocess
import sys
from pathlib import Path

import requests


def get_github_token():
    return os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')


def run_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, shell=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def detect_local_repo_root():
    path = Path(__file__).resolve().parent
    while path != path.parent:
        if (path / '.git').exists():
            return path
        path = path.parent
    raise FileNotFoundError('No .git repository found in current tree')


def get_github_user(token):
    response = requests.get('https://api.github.com/user', headers={'Authorization': f'token {token}'})
    response.raise_for_status()
    return response.json()['login']


def create_repo(token, repo_name, private=True, description='Enterprise CloudOps Automation repository'):
    owner = get_github_user(token)
    payload = {
        'name': repo_name,
        'private': private,
        'description': description,
        'auto_init': False,
        'has_issues': True,
        'has_projects': False,
        'has_wiki': False,
    }
    response = requests.post('https://api.github.com/user/repos', json=payload, headers={'Authorization': f'token {token}'})
    if response.status_code == 422 and 'already exists' in response.text:
        print(f'Repository {owner}/{repo_name} already exists.')
        return owner
    response.raise_for_status()
    print(f'Created GitHub repository: {owner}/{repo_name}')
    return owner


def add_git_remote(repo_root: Path, owner: str, repo_name: str):
    remote_url = f'https://github.com/{owner}/{repo_name}.git'
    try:
        run_command(['git', 'remote', 'add', 'origin', remote_url], cwd=repo_root)
        print(f'Added remote origin: {remote_url}')
    except RuntimeError as exc:
        if 'remote origin already exists' in str(exc):
            print('Remote origin already exists, updating URL to new repository.')
            run_command(['git', 'remote', 'set-url', 'origin', remote_url], cwd=repo_root)
        else:
            raise


def push_main(repo_root: Path):
    print('Pushing main branch to origin...')
    run_command(['git', 'push', '-u', 'origin', 'main'], cwd=repo_root)
    print('Push completed.')


def main():
    token = get_github_token()
    if not token:
        print('ERROR: No GitHub token found. Set GITHUB_TOKEN or GH_TOKEN in your environment.')
        sys.exit(1)

    repo_root = detect_local_repo_root()
    repo_name = repo_root.name
    print(f'Using repo name: {repo_name}')

    owner = create_repo(token, repo_name)
    add_git_remote(repo_root, owner, repo_name)
    push_main(repo_root)


if __name__ == '__main__':
    main()
