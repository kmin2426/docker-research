FROM node:22-bookworm-slim AS node
FROM nvidia/cuda:12.8.1-devel-ubuntu22.04

ARG USER_UID=1000
ARG USER_GID=1000
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm && \
    ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx && \
    npm install -g @openai/codex@latest && \
    mkdir -p /opt/claude-home && \
    curl -fsSL https://claude.ai/install.sh -o /tmp/claude-install.sh && \
    HOME=/opt/claude-home bash /tmp/claude-install.sh && \
    ln -s /opt/claude-home/.local/bin/claude /usr/local/bin/claude && \
    rm -f /tmp/claude-install.sh && npm cache clean --force
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
RUN groupadd --gid "${USER_GID}" researcher && \
    useradd --uid "${USER_UID}" --gid "${USER_GID}" --create-home --shell /bin/bash researcher && \
    mkdir -p /home/researcher/.codex /home/researcher/.claude /home/researcher/.cache/huggingface /home/researcher/.vscode-server && \
    printf 'cli_auth_credentials_store = "file"\n' > /home/researcher/.codex/config.toml && \
    chown -R researcher:researcher /home/researcher
COPY docker/entrypoint.sh /usr/local/bin/research-entrypoint
USER researcher
ENV HOME=/home/researcher CODEX_HOME=/home/researcher/.codex \
    CLAUDE_CONFIG_DIR=/home/researcher/.claude HF_HOME=/home/researcher/.cache/huggingface \
    DISABLE_AUTOUPDATER=1
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/research-entrypoint"]
CMD ["bash"]
