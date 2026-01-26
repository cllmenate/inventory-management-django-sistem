# syntax=docker/dockerfile:1.4
# ==========================================
# STAGE 1: Builder (Instalação de Dependências com uv)
# ==========================================
FROM python:3.13-slim-bookworm AS builder

# Instala o uv (o gerenciador de pacotes mais rápido atualmente)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Variáveis de ambiente para o uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Instala dependências do SO necessárias para compilação (se houver libs C)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependência
COPY pyproject.toml uv.lock ./

# Instala as dependências no ambiente virtual (.venv)
# --frozen garante que o lockfile seja respeitado
# --no-install-project pula a instalação do próprio projeto (será copiado depois)
RUN uv sync --frozen --no-install-project --no-dev

# ==========================================
# STAGE 2: Runtime (Imagem Final)
# ==========================================
FROM python:3.13-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Instala dependências de runtime (libpq para Postgres, netcat para check de saúde)
# Cria um usuário não-root por segurança
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat-openbsd \
    curl \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    fontconfig \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p /home/appuser/.cache && chown -R appuser:appuser /home/appuser

# Define home para o appuser e variáveis de cache
ENV HOME=/home/appuser
ENV XDG_CACHE_HOME=/home/appuser/.cache

# Copia o ambiente virtual do estagio builder
COPY --from=builder /app/.venv /app/.venv

# Copia os scripts de entrada e dá permissão de execução
COPY ./docker/entrypoint.sh /entrypoint.sh
COPY ./docker/prod/start.sh /start.sh
COPY ./docker/prod/worker.sh /worker.sh
RUN chmod +x /entrypoint.sh /start.sh /worker.sh

# Copia o código da aplicação
COPY . /app

# Cria diretórios necessários e ajusta permissões
RUN mkdir -p /app/staticfiles /app/mediafiles /app/mediafiles/temp \
    && chown -R appuser:appuser /app /app/staticfiles /app/mediafiles

# Define o usuário para execução
USER appuser

# Define o PATH para incluir o venv
ENV PATH="/app/.venv/bin:$PATH"

# Define o WORKDIR
WORKDIR /app

# Healthcheck (Overridden in docker-compose.yml for specific services)
HEALTHCHECK --interval=60s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/schema/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]
