# Casos de Uso

Este documento detalha o fluxo de interação e a lógica de negócio para os principais cenários do sistema.

---

## 🗂️ 1. Homologação de Novo Produto

**Ator**: Gestor de Estoque  
**Resumo**: Processo de introdução de um novo item no catálogo, garantindo que todas as dependências (Marca, Categoria, Modelo) existam corretamente.

```mermaid
sequenceDiagram
    participant Gestor
    participant API
    participant DB

    Gestor->>API: POST /brands/ (Cria Marca)
    API->>DB: Salva Marca
    Gestor->>API: POST /categories/ (Cria Categoria)
    API->>DB: Salva Categoria
    Gestor->>API: POST /product-models/ (Cria Modelo)
    API->>DB: Salva Modelo (Link com Marca)
    Gestor->>API: POST /products/ (Cria Produto)
    API->>DB: Salva Produto (Link com Modelo/Categoria)
    API-->>Gestor: Produto Homologado com Sucesso
```

---

## 📥 2. Recebimento de Carga (Inflow)

**Ator**: Operador de Logística  
**Resumo**: Registro de entrada de mercadoria fornecida por um parceiro externo, resultando no incremento automático do saldo em estoque.

```mermaid
sequenceDiagram
    participant Operador
    participant API
    participant Sign as Signal/Logic
    participant DB

    Operador->>API: POST /inflows/ (Produto, Qtd, Fornecedor)
    API->>DB: Salva registro de Entrada
    API->>Sign: Dispara atualização de estoque
    Sign->>DB: UPDATE products SET quantity = quantity + inflow_qtd
    DB-->>API: Saldo Atualizado
    API-->>Operador: Entrada Registrada e Saldo Atualizado
```

---

## 📊 3. Auditoria Mensal de Inventário

**Ator**: Analista de Dados  
**Resumo**: Extração de dados para conferência externa. Utiliza processamento assíncrono para lidar com grandes volumes de dados sem impactar a performance.

```mermaid
sequenceDiagram
    participant Analista
    participant API
    participant Celery
    participant Notif as Notificação

    Analista->>API: Solicita Export (PDF/Excel)
    API->>Celery: Despacha tarefa (Async)
    API-->>Analista: "Solicitação Recebida (ID: #123)"
    
    Note over Celery: Processando dados pesados...
    
    Celery->>Notif: Marca tarefa como "Concluída"
    Analista->>API: Consulta notificações
    API-->>Analista: Link para Download liberado
```

---

## 📈 Diagrama Geral de Atores

Abaixo está a visão consolidada de acesso por perfil:

```mermaid
flowchart TD
    admin((Administrador))
    gestor((Gestor))
    op((Operador))
    ana((Analista))

    subgraph "Sistema de Gestão"
        UC1([Gestão de Usuários])
        UC2([Setup de Produtos])
        UC3([Movimentar Estoque])
        UC4([Extração de Dados])
    end

    admin --- UC1
    admin --- UC2
    admin --- UC3
    admin --- UC4
    
    gestor --- UC2
    op --- UC3
    ana --- UC4
```
