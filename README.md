# docker-research

A Docker and VS Code Dev Container template for machine learning research.

## Setup

Install Docker, Compose, VS Code with Dev Containers, and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). A compatible NVIDIA GPU and driver are required to run the container.

```bash
python3 scripts/init.py
```

Example:

```text
Project name: my-research
Author: Dongmin Kim
Author email: dongmin.kim@example.com
License:
  1) MIT
  2) Apache-2.0
  3) BSD-3-Clause
  4) GPL-3.0-only
  5) Empty LICENSE
Select a number: 5
Add README? (yes/no): yes
```
After initialization, the folder is renamed to the project name and `scripts/` is removed; the GitHub Actions workflow remains. Run `cd ../<project-name>` to update your shell path. Each collaborator configures their own `.env` using `.env.example`.

```bash
./.devcontainer/build.sh
./.devcontainer/run.sh
```


## Authentication

Run `codex` and `claude` in the container and sign in.

Login and local session data persist across rebuilds.
`docker compose down -v` deletes this data.

## CI

Every branch push builds the Docker image. A successful push to `main` publishes it to `ghcr.io/<owner>/<repository>` using `GITHUB_TOKEN`.

## License

See [LICENSE](LICENSE). When selecting a non-MIT license during initialization, the original template's MIT notice is preserved in `NOTICE`.
