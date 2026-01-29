# Guia de Desenvolvimento e QA

Este documento detalha os padrões de qualidade e procedimentos de teste do sistema.

## 🛠️ Ambiente de Desenvolvimento

### Gerenciamento com UV

O projeto utiliza o **Astral UV**, que é significativamente mais rápido que o `pip` e gerencia ambientes virtuais automaticamente.

- **Sincronizar ambiente**: `uv sync`
- **Adicionar dependência**: `uv add <package>`
- **Rodar comando no venv**: `uv run <command>`

### Variáveis de Ambiente (.env)

Configurações críticas em `app/settings.py` dependem do `.env`:

- `DEBUG`: `True` em dev, `False` em prod.
- `SECRET_KEY`: Chave de segurança do Django.
- `SIGNING_KEY`: Chave para assinatura de tokens JWT.
- `POSTGRES_DB/...`: Credenciais do banco.

## 🧪 Estratégia de Testes

Utilizamos **Pytest** com uma suíte de testes robusta que cobre unitários, integração e comportamento.

### Execução de Testes

```bash
# Execução padrão
uv run pytest

# Verificação de cobertura (Coverage)
uv run pytest --cov=. --cov-report=html
```

### Categorias de Testes

- **Unitários**: Testam modelos e lógica isolada (ex: `tests/products/test_models.py`).
- **Integração**: Testam o fluxo entre camadas (ex: logic -> database -> cache).
- **API (Request Tests)**: Testam os endpoints DRF (ex: `tests/api/v1/`).
- **Signals**: Verificam se o estoque é atualizado corretamente após uma entrada/saída.

### Mocking e Utilidades

- **Factory Boy**: Usado para gerar dados de teste consistentes sem escrita manual de objetos.
- **Time-machine**: Usado para testar comportamentos que dependem da data/hora (ex: relatórios diários).
- **Database**: O ambiente de testes utiliza **SQLite em memória** por padrão para velocidade, configurado no `pyproject.toml` via `pytest-env`.

## 💎 Qualidade de Código (Linting)

Não aceitamos código sem validação de estilo e tipos.

### Ruff (Linter & Formatter)

Substitui o Flake8, Black e Isort com desempenho muito superior.

```bash
uv run ruff check .  # Lint
uv run ruff format . # Format
```

### MyPy (Type Checking)

Garante que a tipagem estática do Python seja respeitada, reduzindo erros de runtime.

```bash
uv run mypy .
```

### Pre-commit Hooks

Configurado para rodar antes de cada `git commit`:

- Limpeza de espaços em branco.
- Check de arquivos YAML/JSON.
- Verificação de secrets (prevenção de vazamento de chaves).
- Execução rápida do Ruff.
