# Visão Geral do Projeto

O **Sistema de Gestão de Estoque** é uma solução empresarial robusta desenvolvida para centralizar e otimizar o controle de inventário. O projeto nasceu da necessidade de um sistema que combinasse a facilidade de uso de um monólito com a escalabilidade de processos assíncronos modernos.

## 🎯 Nossa Visão

Proporcionar aos gestores uma visão clara e em tempo real de seus ativos, minimizando perdas por vencimento, falta de estoque ou falhas operacionais. O sistema é construído sobre pilares de **auditabilidade**, **desempenho** e **segurança**.

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Papel |
| :--- | :--- | :--- |
| **Backend** | Django 5.2 | Framework principal e ORM |
| **API** | REST Framework | Camada de comunicação stateless |
| **Documentação API** | drf-spectacular | Geração de esquema OpenAPI 3.0 |
| **Banco de Dados** | PostgreSQL 17 | Persistência de dados relacional |
| **Cache & Broker** | Redis | Cache de métricas e tarefas Celery |
| **Async Tasks** | Celery & Beat | Processamento de relatórios e agendamentos |
| **Interface** | HTML/Vanilla CSS | Frontend responsivo servido pelo Django |
| **Monitoramento** | Sentry SDK | Rastreamento de erros e performance |

## 📂 Estrutura Modular

O projeto é dividido em aplicações Django independentes (apps), permitindo uma manutenção isolada:

- **Core Apps**: `products`, `brands`, `categories`, `product_models`.
- **Movimentação**: `inflows` (entradas), `outflows` (saídas).
- **Serviços**: `notifications` (rastreio de tarefas), `authentication` (JWT).
- **Infra**: `nginx` (proxy), `docker` (conteinerização).

---

### [Explorar Funcionalidades](features.md) | [Guia de Arquitetura](architecture.md) | [Começar Desenvolvimento](development.md) | [Casos de Uso](use-cases.md)
