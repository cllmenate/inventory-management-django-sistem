# Desenvolvimento

Este guia aborda as práticas de configuração de ambiente, fluxo de desenvolvimento e padrões do projeto.

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.13+
- Docker & Docker Compose
- Git
- `uv` (Gerenciador de pacotes)

### Setup Local

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/cllmenate/inventory-management-django-sistem.git
   cd inventory-management-django-system
   ```

2. **Instale as dependências com `uv`:**

   ```bash
   uv sync --dev
   ```

3. **Configure o `.env`:**
   Copie o exemplo e ajuste conforme necessário.

   ```bash
   cp .env.example .env
   ```

4. **Suba o banco de dados via Docker:**

   ```bash
   docker-compose up -d inventory_db inventory_redis
   ```

5. **Rode as migrações:**

   ```bash
   uv run python manage.py migrate
   ```

6. **Execute o servidor local:**
   ```bash
   uv run python manage.py runserver
   ```

## Guidelines e Padrões

Seguimos estritamente os padrões da comunidade Python e Django.

### Linting e Formatação

Utilizamos **Ruff** para garantir a qualidade do código.

- **Lint:** `uv run ruff check .`
- **Format:** `uv run ruff format .`

### Tipagem Estática

Utilizamos **MyPy** para garantir a segurança de tipos.

- **Check:** `uv run mypy .`

### Hooks de Git

O **Pre-commit** roda automaticamente antes de cada commit para verificar linting, trailing whitespaces e chaves secretas.

- Instalar hooks: `uv run pre-commit install`

## Testes Automatizados

O projeto utiliza **Pytest** como runner de testes.

### Executando Testes

```bash
# Rodar todos os testes
uv run pytest

# Rodar com cobertura
uv run pytest --cov=app
```

### Estrutura de Testes

Os testes estão localizados na pasta `tests/` e espelham a estrutura das apps.

- `tests/authentication/`: Testes de login e permissões.
- `tests/products/`: Testes de CRUD de produtos.
- `tests/integration/`: Testes de integração de API.
