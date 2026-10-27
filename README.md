# docker-research

A reusable CUDA and PyTorch development environment for machine learning and AI research. No ROS dependencies.

## Prerequisites

- Docker Engine, Docker Compose V2, VS Code, and the Dev Containers extension.
- An NVIDIA GPU, compatible host driver, and [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) to run the container with GPU access.

The image uses CUDA 12.8 and PyTorch 2.7.1. CUDA 12.8 supports Blackwell according to the [NVIDIA architecture matrix](https://docs.nvidia.com/datacenter/tesla/drivers/cuda-toolkit-driver-and-architecture-matrix.html); the wheel is listed in the [PyTorch installation guide](https://pytorch.org/get-started/previous-versions/). Check compatibility for your GPU, driver, and any additional CUDA extensions.

## Setup and use

```bash
python3 scripts/init.py
# Enter a unique project name, author, email, license, and README choice.
./scripts/build.sh
./scripts/run.sh
```

The initializer writes project metadata to `project.json`, sets the local image to `<project-name>:latest`, and creates `.env` with the Compose project name and host UID/GID. Choose a unique name for each checkout on the Docker host; checkouts with the same name share containers and volumes. The README choice replaces this template guide with a minimal project README, or removes it if you answer no. Save a copy first if you need these instructions. The initializer refuses to overwrite an existing `.env` or `project.json`. Choose MIT, Apache-2.0, BSD-3-Clause, GPL-3.0-only, or a custom license file by entering its number. For a non-MIT choice, the original template remains MIT licensed and its notice is retained in `LICENSE.template`; the chosen license applies to your additions. Alternatively, copy `.env.example` to `.env` and edit it manually. Set nonzero UID and GID values that do not conflict with existing image users or groups. Changing them after creating a volume may require fixing its ownership. Docker Desktop file permissions can differ from Linux.

Alternatively, open this folder in VS Code and select **Dev Containers: Reopen in Container**. Use **Dev Containers: Rebuild Container** after changing dependencies or configuration. The terminal runs as `researcher` in `/workspace`. The Python, Codex, and Claude Code extensions are installed in the container.

Inside the container:

```bash
python3 -c 'import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())'
nvidia-smi
codex --version
claude --version
```

Manage PyTorch and other Python packages in `requirements.txt`, then rebuild. Building does not require a GPU; running the Compose service requires the NVIDIA runtime.

## Authentication and persistent state

Run `codex` and `claude` in the container and follow their login prompts. Credentials are never baked into the image. Codex uses [file-based credential storage](https://developers.openai.com/codex/auth) under `CODEX_HOME`; Claude uses `CLAUDE_CONFIG_DIR`. Codex is installed using the [official npm method](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) and Claude using its [native installer](https://code.claude.com/docs/en/setup). Claude automatic updates are disabled; rebuild to update it.

The project-scoped `research-home` volume persists `/home/researcher`, including CLI credentials, settings and local sessions, `~/.claude.json`, the Hugging Face cache, and VS Code Server state under `~/.vscode-server/data/User/{globalStorage,workspaceStorage}`. The workspace is bind-mounted; `datasets/` and `outputs/` remain on the host. These paths survive a normal rebuild or `docker compose down`.

Extension storage locations are not a stable public contract. Host-side VS Code state, OS keyrings, cloud history, expired or revoked tokens, deleted conversations, and running processes are not guaranteed to survive. Organization policy may require keyring authentication. See the [Codex IDE](https://developers.openai.com/codex/ide) and [Claude Code VS Code](https://code.claude.com/docs/en/vs-code) documentation; back up important records separately.

The volume contains credentials and conversations: protect access to the Docker host and backups. **`docker compose down -v` deletes the volume and its contents.** Changing the Compose project name selects a different volume. Data, outputs, credentials, and caches are excluded from Git and the build context; ignore rules do not remove already tracked files.

## CI and GHCR

Every branch push builds the image using GitHub Actions cache. A successful push to `main` also publishes `ghcr.io/<owner>/<repository>:latest` and `:sha-<full-commit-sha>`. The workflow uses `GITHUB_TOKEN` with `contents: read` and `packages: write`; no personal access token is needed. Enable package write access in repository Actions settings and manage package visibility in GHCR. GitHub-hosted runners do not run GPU inference.

## License

See [LICENSE](LICENSE).
