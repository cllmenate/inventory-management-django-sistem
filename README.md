# Sistema de Gestão de Estoque

![Python Version](https://img.shields.io/badge/python-3.13-blue)
![Django Version](https://img.shields.io/badge/django-6.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Um sistema completo de gestão de inventário focado em rastreabilidade de produtos, fornecedores e movimentações financeiras.

## 🚀 Tecnologias

- **Backend**: Python 3.13, Django 6.0, Django Rest Framework
- **Banco de Dados**: PostgreSQL
- **Cache & Filas**: Redis, Celery
- **Infraestrutura**: Docker, Docker Compose
- **Qualidade**: Pytest, Ruff, MyPy, Pre-commit
- **Documentação**: MkDocs, Drf-spectacular (Swagger/ReDoc)

## 📚 Documentação

- **[Documentação Completa](docs/index.md)**: Guias de arquitetura, instalação e contribuição.
- **API Swagger**: `/api/v1/docs/`
- **ReDoc**: `/api/v1/redoc/`

## 🛠️ Instalação Rápida

### Opção 1: Docker (Recomendado)

1. Clone o repositório:

   ```bash
   git clone https://github.com/seurepositorio/inventory-management.git
   cd inventory-management-django-system
   ```

2. Crie o arquivo `.env`:

   ```bash
   cp .env.example .env
   ```

3. Suba os containers:
   ```bash
   docker-compose up -d --build
   ```

O sistema estará disponível em: `http://localhost:8000`

### Opção 2: Desenvolvimento Local

1. Instale o [uv](https://github.com/astral-sh/uv):

   ```bash
   pip install uv
   ```

2. Instale as dependências:

   ```bash
   uv sync
   ```

3. Ative o ambiente virtual:

   ```bash
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

4. Configure o banco de dados e rode as migrações:

   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## 🧪 Rodando os Testes

Para garantir a integridade do sistema, execute os testes com `pytest`:

```bash
uv run pytest
```

Para gerar cobertura de testes:

```bash
uv run pytest --cov=app --cov-report=html
```

## 🤝 Contribuição

Consulte o [Guia de Contribuição](docs/contributing.md) para detalhes sobre nosso fluxo de desenvolvimento.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autores / Contato

* **Nattam Pereira** - *Portfólio* - [GitHub](https://github.com/cllmenate) - Copyright (c) 2026