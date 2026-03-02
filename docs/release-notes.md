# Release Notes

## [v1.1.1] - 2026-03-02

### 🐛 Correções (Hotfixes)

- **Estabilidade e Qualidade**: Fortalecimento da tipagem estática do projeto com MyPy para previnir bugs na camada de serviços genéricos de importação/exportação.
- **Refatorações e Code Smells**: Resolução de métricas do SonarQube mitigando Alta Complexidade Cognitiva de métodos massivos e otimizando fluxos de forms.
- **Code Style**: Alinhamento rigoroso à regras de formatação PEP8 de 79 caracteres via Ruff e Flake8.

---

## [v1.1.0] - 2026-01-27

Esta versão traz melhorias significativas na visibilidade operacional do sistema, com foco em notificações e relatórios.

### ⭐ Novidades

- **Módulo de Notificações**: Rastreamento de tarefas assíncronas de exportação e importação.
- **Exportação Assíncrona**: Suporte a formatos CSV, PDF, JSON e XML para todos os principais modelos.
- **Dashboard Metrics Cache**: Métricas do dashboard agora são recalculadas via Celery Beat para performance instantânea.
- **Monitoramento**: Integração com Sentry para rastreio de erros em tempo real.

### 🛠️ Técnico

- Atualização para Django 5.2.
- Adição de `Pandas` e `WeasyPrint` para processamento de dados e PDF.
- Configuração de `django-celery-beat` e `django-celery-results`.
- Melhoria nos healthchecks do Docker.

---

## [v1.0.1] - 2026-01-19

### 🐛 Correções

- Fix no Mermaid Rendering no MkDocs.
- Melhoria na sidebar e links do admin.

---

## [v1.0.0] - 2026-01-16

- Lançamento inicial.
