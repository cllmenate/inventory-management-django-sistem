# Guia de Arquitetura

Este documento fornece um aprofundamento técnico sobre a infraestrutura e o fluxo de dados do sistema.

## 🏗️ Topologia da Infraestrutura

O sistema utiliza uma arquitetura de serviços coordenados via Docker Compose, garantindo isolamento e escalabilidade horizontal para os workers.

```mermaid
graph LR
    User[Usuário] -->|HTTPS| Nginx["Nginx (Proxy Reverso)"]
    Nginx -->|Port 8000| Gunicorn["Gunicorn (Django)"]
    
    subgraph "Core System"
        Gunicorn --> DB[(PostgreSQL 17)]
        Gunicorn --> Redis[(Redis)]
    end

    subgraph "Background Processing"
        Redis --> Worker["Celery Worker (Tasks)"]
        Worker --> DB
        Beat["Celery Beat (Schedule)"] --> Redis
    end

    subgraph "Observability"
        Gunicorn -.-> Sentry[Sentry.io]
        Worker -.-> Sentry
    end
```

## 🐳 Componentes Docker

O sistema roda em containers isolados que se comunicam via rede interna.

```mermaid
graph TB
    subgraph "Host Machine"
        subgraph "Docker Network: inventory_network"
            Nginx["nginx:alpine<br/>inventory_nginx<br/>Port: 80→80"]
            Web["python:3.13-slim<br/>inventory_web<br/>Port: 8000"]
            Worker["python:3.13-slim<br/>inventory_worker"]
            Beat["python:3.13-slim<br/>inventory_beat"]
            Flower["python:3.13-slim<br/>inventory_flower<br/>Port: 5555"]
            DB["postgres:17-alpine<br/>inventory_db<br/>Port: 5432"]
            Redis["redis:7-alpine<br/>inventory_redis<br/>Port: 6379"]
        end
        
        Volumes["Volumes (Persistent)<br/>postgres_data<br/>redis_data<br/>media_volume"]
    end

    Nginx -->|Proxy Pass :8000| Web
    Nginx -->|Serve /static/| Volumes
    Nginx -->|Serve /media/| Volumes
    Web --> DB
    Web --> Redis
    Worker --> DB
    Worker --> Redis
    Beat --> Redis
    Flower --> Redis
    DB -.->|Persists| Volumes
    Redis -.->|Persists| Volumes
    Web -.->|Uploads| Volumes
```

### Health Checks

Cada serviço possui verificações de saúde:

```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## 📊 Modelo de Dados (ERD)

A estrutura do banco de dados é projetada para integridade referencial total.

```mermaid
erDiagram
    Product ||--o{ Inflow : "recebe"
    Product ||--o{ Outflow : "emite"
    Brand ||--o{ ProductModel : "possui"
    ProductModel ||--o{ Product : "define"
    Category ||--o{ Product : "classifica"
    Supplier ||--o{ Inflow : "fornece"
    User ||--o{ TaskNotification : "recebe"

    Product {
        string title
        string serial_number
        decimal cost_price
        decimal sell_price
        int quantity
    }
    
    TaskNotification {
        string task_id
        string status
        string task_type
        datetime completed_at
    }
```

## 🔄 Lifecycle de Tarefas Assíncronas

As tarefas de exportação/importação seguem um fluxo de estados gerenciado pelo Celery e rastreado no banco de dados.

```mermaid
stateDiagram-v2
    [*] --> Pendente: Usuário solicita Export
    Pendente --> Processando: Worker captura tarefa
    Processando --> Concluido: Sucesso (Arquivo gerado)
    Processando --> Falha: Erro capturado
    Concluido --> [*]
    Falha --> Pendente: Retry (opcional)
    Falha --> [*]
```

## ⚙️ Componentes de Infraestrutura

### Nginx (Proxy Reverso)

O Nginx atua como a primeira camada de defesa e otimização:

- **Proxy Pass**: Encaminha requisições dinâmicas para o Gunicorn.
- **Static Serving**: Serve diretamente os arquivos em `/staticfiles/` sem onerar o Django.
- **Media Serving**: Gerencia o download de arquivos protegidos em `/mediafiles/` (como exports gerados).
- **Docs Hosting**: Serve esta documentação estática (MKDocs) em `/docs/`.

### Celery & Redis

- **Broker**: O Redis armazena a fila de mensagens.
- **Worker**: Processa tarefas `shared_task` (exports, imports).
- **Beat**: Um agendador que dispara tarefas periódicas (ex: `update_dashboard_metrics_cache` a cada 5 minutos).
- **Result Backend**: Utilizamos `django-db` para persistir o histórico de resultados das tarefas, permitindo que o usuário veja o status em "Notificações".

### Monitoramento com Sentry

Configurado em `app/settings.py`, o Sentry captura:

- Exceções não tratadas (500 errors).
- Gargalos de performance em queries SQL.
- Erros em tarefas assíncronas do Celery.

---

## 🔐 Camadas de Segurança

```mermaid
flowchart TD
    A[Internet] --> B{Nginx}
    B -->|CORS Check| C[Django Security Middleware]
    C --> D{Authentication}
    D -->|JWT Valid?| E[DRF Permissions]
    D -->|Invalid| F[401 Unauthorized]
    E -->|IsAdmin/IsStaff| G[Admin Dashboard]
    E -->|Model Permissions| H[API Resource]
```

### Fluxo de Autenticação (JWT)

O sistema utiliza `rest_framework_simplejwt`:

1. **Login**: O cliente envia credenciais e recebe `access` e `refresh` tokens.
2. **Access Token**: Curta duração (30 min), enviado no header `Authorization: Bearer <token>`.
3. **Refresh Token**: Longa duração (7 dias), usado para obter um novo `access` sem re-autenticar.
4. **Blacklist**: Ao deslogar (logout), o token é colocado em uma blacklist no banco de dados.

```mermaid
sequenceDiagram
    participant Cliente
    participant API as API (Django)
    participant DB as Banco de Dados

    Cliente->>API: POST /token/ (username, password)
    API->>DB: Verifica credenciais
    alt Credenciais Válidas
        DB-->>API: Usuário encontrado
        API-->>Cliente: Retorna Access + Refresh Tokens
    else Credenciais Inválidas
        API-->>Cliente: 401 Unauthorized
    end

    Note over Cliente, API: Uso do token em requisições
    Cliente->>API: GET /products/ (Header: Bearer <access_token>)
    API->>API: Valida assinatura do token
    alt Token Válido
        API-->>Cliente: 200 OK (Dados dos produtos)
    else Token Expirado/Inválido
        API-->>Cliente: 401 Unauthorized
    end
```

## 📊 Estratégia de Caching

Para garantir que o dashboard seja carregado em milissegundos, utilizamos cache agressivo no Redis:

- **Métricas Globais**: Armazenadas como chaves JSON `metrics:product`, `metrics:sales`, etc.
- **Invalidação**: O cache é renovado pelo Celery Beat ou via signals em alterações críticas.
