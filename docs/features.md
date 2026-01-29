# Funcionalidades do Sistema

Esta página detalha as capacidades técnicas e operacionais de cada módulo do sistema, acompanhadas de seus respectivos diagramas de uso.

---

## 📦 Gestão de Produtos

**Resumo**: Este módulo é o coração do sistema, permitindo o cadastro e organização de itens de estoque com suporte a hierarquia de marcas, categorias e modelos.

```mermaid
flowchart TD
    gestor((Gestor de Estoque))
    subgraph "Módulo: Produtos"
        UC1([Cadastrar Marca/Categoria])
        UC2([Definir Modelo Técnico])
        UC3([Gerenciar SKU/Produto])
        UC4([Consultar Saldo])
    end
    gestor --- UC1
    gestor --- UC2
    gestor --- UC3
    gestor --- UC4
```

---

## 📥 Entradas (Inflows)

**Resumo**: Gerencia a reposição de estoque. Cada entrada registra a quantidade recebida, o fornecedor responsável e atualiza o saldo do produto automaticamente.

```mermaid
flowchart TD
    op((Operador de Logística))
    subgraph "Módulo: Entradas"
        UC1([Registrar Recebimento])
        UC2([Vincular Fornecedor])
        UC3([Validar NF/Observações])
    end
    op --- UC1
    op --- UC2
    op --- UC3
```

---

## 📤 Saídas (Outflows)

**Resumo**: Controla a baixa de mercadorias. O sistema valida se há saldo suficiente antes de confirmar a saída, garantindo a integridade do inventário.

```mermaid
flowchart TD
    op((Operador de Logística))
    subgraph "Módulo: Saídas"
        UC1([Registrar Venda/Baixa])
        UC2([Validar Disponibilidade])
        UC3([Atualizar Saldo])
    end
    op --- UC1
    op --- UC2
    op --- UC3
```

---

## 🔔 Notificações e Tarefas Assíncronas

**Resumo**: Gerencia processos pesados em background (Celery). O usuário solicita uma operação e é notificado quando o resultado está pronto.

```mermaid
flowchart TD
    user((Usuário Autenticado))
    subgraph "Módulo: Notificações"
        UC1([Solicitar Exportação])
        UC2([Acompanhar Status Task])
        UC3([Download de Arquivos])
    end
    user --- UC1
    user --- UC2
    user --- UC3
```

---

## 📊 Relatórios Dinâmicos

**Resumo**: Transforma dados brutos em inteligência de negócio através de dashboards em tempo real e exportações formatadas.

```mermaid
flowchart TD
    ana((Analista))
    subgraph "Módulo: Relatórios"
        UC1([Visualizar Dashboard])
        UC2([Gerar Listagem PDF])
        UC3([Exportar para Excel/CSV])
    end
    ana --- UC1
    ana --- UC2
    ana --- UC3
```
