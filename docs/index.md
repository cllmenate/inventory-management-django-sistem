# Visão Geral do Projeto

Bem-vindo à documentação oficial do **Sistema de Gestão de Estoque**.

Este é um sistema robusto desenvolvido para empresas que necessitam controlar seu inventário de forma eficiente. Ele permite o cadastro de produtos, fornecedores, marcas, categorias e o registro detalhado de todas as movimentações de entrada e saída.

## 🚀 Funcionalidades Principais

- **Gestão de Produtos**: Controle total sobre o catálogo de itens.
- **Entradas e Saídas**: Registro fiscal e físico de movimentações.
- **Controle de Estoque**: Atualização automática de quantidades.
- **Dashboards**: Visualização de métricas (implementação futura).
- **API REST**: Pronta para integração com mobile e outros sistemas.

## 📂 Estrutura do Projeto

Abaixo, a estrutura de diretórios explicada para desenvolvedores:

```ascii
inventory-management-django-system/
├── app/                    # Configurações principais do Django (settings, urls)
├── authentication/         # App de Usuários e Autenticação (JWT)
├── brands/                 # App de Marcas
├── categories/             # App de Categorias
├── product_models/         # App de Modelos de Produtos
├── products/               # App de Produtos (Core do sistema)
├── suppliers/              # App de Fornecedores
├── inflows/                # App de Entradas de Estoque
├── outflows/               # App de Saídas de Estoque
├── docker/                 # Scripts e Dockerfiles auxiliares
├── docs/                   # Documentação do projeto (MKDocs)
├── nginx/                  # Configuração do Proxy Reverso
├── tests/                  # Testes automatizados (Pytest)
├── db.sqlite3              # Banco local (apenas para dev rápido)
├── docker-compose.yml      # Orquestração para Desenvolvimento
├── docker-compose.prod.yml # Orquestração para Produção
├── manage.py               # CLI do Django
├── pyproject.toml          # Gerenciamento de dependências (UV)
└── README.md               # Guia Rápido
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.13, Django 6.0
- **API**: Django Rest Framework (DRF)
- **Documentação**: Drf-spectacular (OpenAPI 3) & MkDocs
- **Banco de Dados**: PostgreSQL 17
- **Cache**: Redis
- **Infraestrutura**: Docker & Docker Compose
