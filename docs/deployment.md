# Deploy

Este guia cobre o processo de deploy da aplicação utilizando Docker.

## Docker em Produção

A aplicação é totalmente conteinerizada e pronta para rodar em qualquer ambiente que suporte Docker (AWS ECS, DigitalOcean App Platform, Servidor VPS, etc.).

### Arquivos de Configuração

- `Dockerfile`: Multi-stage build para criar imagens leves e seguras.
- `docker-compose.prod.yml`: Orquestração dos serviços para produção (Web, Worker, Nginx, DB, Redis).
- `.env.prod`: Variáveis de ambiente específicas de produção.

### Passo a Passo para Deploy

1. **Configurar Variáveis de Meio Ambiente:**
   Crie um arquivo `.env.prod` com as credenciais reais do banco de dados e chaves secretas. **NUNCA commite este arquivo.**

2. **Build e Execução:**

   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

3. **Verificação de Saúde:**
   O Docker Compose possui `healthchecks` configurados. Verifique se os serviços estão saudáveis:

   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

4. **Arquivos Estáticos e Media:**
   O Nginx é configurado para servir arquivos estáticos e media volumes compartilhados. O container `inventory_web` roda o `collectstatic` automaticamente no script de entrada.

### Nginx como Proxy Reverso

Utilizamos o Nginx na frente da aplicação Python (Uvicorn/Gunicorn) para:

- Servir arquivos estáticos (CSS, JS, Imagens).
- Servir a documentação estática (MKDocs).
- Adicionar headers de segurança.
- Fazer balanceamento de carga (se houver múltiplas réplicas).

### CI/CD

O projeto conta com um workflow do GitHub Actions (`ci-cd.yml`) que roda os testes e linters a cada push. Para deploy contínuo, este workflow pode ser estendido para fazer push da imagem Docker para um Container Registry (ex: Docker Hub, ECR).
