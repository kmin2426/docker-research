#!/usr/bin/env python3
"""Initialize a new checkout without overwriting an existing setup."""
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import sys

root = Path(__file__).resolve().parent.parent
os.chdir(root)


def ask(prompt, default=''):
    suffix = f' [{default}]' if default else ''
    value = input(f'{prompt}{suffix}: ').strip() or default
    if not value:
        raise ValueError(f'{prompt} is required')
    return value


def main():
    if Path('.env').exists() or Path('project.json').exists():
        raise ValueError('.env or project.json already exists; initialization would overwrite it')
    name = ask('Project name (lowercase letters, digits, hyphens, underscores)', root.name.lower())
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name):
        raise ValueError('Project name must start with a lowercase letter or digit and contain only lowercase letters, digits, hyphens, and underscores')
    target = root.parent / name
    if target != root and target.exists():
        raise ValueError(f'Cannot rename project: {target} already exists')
    if target != root and not os.access(root.parent, os.W_OK | os.X_OK):
        raise ValueError(f'Cannot rename project: no write access to {root.parent}')
    author = ask('Author')
    email = ask('Author email')
    if any(c in author + email for c in '\r\n') or not re.fullmatch(r'[^\s@]+@[^\s@]+', email):
        raise ValueError('Enter a valid single-line author and email')
    print('License:\n  1) MIT\n  2) Apache-2.0\n  3) BSD-3-Clause\n  4) GPL-3.0-only\n  5) Empty LICENSE')
    choice = ask('Select a number', '1')
    original = Path('LICENSE').read_text(encoding='utf-8').rstrip()
    licenses = {'2': 'Apache-2.0', '3': 'BSD-3-Clause', '4': 'GPL-3.0-only'}
    if choice == '1':
        license_name = 'MIT'
        line = f'Copyright (c) {datetime.date.today().year} {author}'
        license_text = original.replace('\n\nPermission is hereby granted', f'\n{line}\n\nPermission is hereby granted', 1) + '\n'
    elif choice in licenses:
        license_name = licenses[choice]
        license_text = Path(f'scripts/licenses/{license_name}.txt').read_text(encoding='utf-8')
        if choice == '3':
            license_text = license_text.replace('{year}', str(datetime.date.today().year)).replace('{author}', author)
    elif choice == '5':
        license_name = 'Unspecified'
        license_text = ''
    else:
        raise ValueError('Choose a number from 1 to 5')
    if choice != '1' and Path('NOTICE').exists():
        raise ValueError('NOTICE already exists; initialization would overwrite it')
    readme = ask('Add README? (yes/no)', 'yes').lower()
    if readme not in ('yes', 'y', 'no', 'n'):
        raise ValueError('Answer yes or no')
    uid = os.getuid() if hasattr(os, 'getuid') else 1000
    gid = os.getgid() if hasattr(os, 'getgid') else 1000
    if uid == 0 or gid == 0:
        raise ValueError('Run as a non-root user so workspace files use your UID and GID')
    metadata = {'name': name, 'author': author, 'email': email, 'license': license_name}
    env = f'PROJECT_NAME={name}\nCOMPOSE_PROJECT_NAME={name}\nUSER_UID={uid}\nUSER_GID={gid}\n'
    # Validate all inputs before modifying any files.
    Path('project.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('.env').write_text(env, encoding='utf-8')
    if choice != '1':
        Path('NOTICE').write_text('Original template license:\n\n' + original + '\n', encoding='utf-8')
    Path('LICENSE').write_text(license_text, encoding='utf-8')
    if readme in ('yes', 'y'):
        Path('README.md').write_text(f'''# {name}

## Setup

Install Docker, Docker Compose, VS Code with Dev Containers, and the NVIDIA Container Toolkit. A compatible NVIDIA GPU and driver are required.

```bash
./.devcontainer/build.sh
./.devcontainer/run.sh
```

Alternatively, open this folder in VS Code and select **Dev Containers: Reopen in Container**. After changing dependencies, use **Dev Containers: Rebuild Container**. Add Python dependencies to `requirements.txt`.

## Authentication and data

Run `codex` and `claude` in the container and sign in. Local sessions and credentials persist in the project Docker volume across rebuilds. `docker compose down -v` deletes the volume. Extension and external service state may not persist; back up important records.

## CI

Pushes build the Docker image. Pushes to `main` also publish it to GHCR using `GITHUB_TOKEN`.
''', encoding='utf-8')
    else:
        Path('README.md').unlink(missing_ok=True)
    if target != root:
        root.rename(target)
    shutil.rmtree('scripts')
    print(f'Initialized {name}: image {name}:latest, Compose project {name}.')
    if target != root:
        print(f'Directory renamed to {target}. Run: cd ../{name}')
    print('Review LICENSE and project.json, then run ./.devcontainer/build.sh or open the Dev Container.')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nInitialization cancelled.', file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as exc:
        print(f'Initialization failed: {exc}', file=sys.stderr)
        sys.exit(1)
