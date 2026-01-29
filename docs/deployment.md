# Deploy e DevOps

Este guia aborda o ciclo de vida de produção e as operações do sistema.

## 🚀 Produção com Docker Compose

O arquivo `docker-compose.prod.yml` é otimizado para produção:

- **Imagens**: Utiliza o stage `runtime` do Dockerfile, resultando em imagens de ~150MB.
- **Segurança**: Roda com usuário não-root (`appuser`).
- **Restart Policy**: `unless-stopped` para alta disponibilidade.
- **Logs**: Rotação de logs configurada para evitar estouro de disco.

### Comandos de Deploy

```bash
# Build e Deploy
docker-compose -f docker-compose.prod.yml up -d --build

# Verificar logs
docker-compose -f docker-compose.prod.yml logs -f inventory_web
```

## 🔄 Pipeline de CI/CD (GitHub Actions)

Localizado em `.github/workflows/ci-cd.yml`, o pipeline garante que:

1. **Linting**: Ruff e MyPy validam o estilo.
2. **Security**: `detect-secrets` verifica vazamentos de chaves.
3. **Testes**: Pytest roda toda a suíte de testes.
4. **Deploy Automático**: (Opcional) Trigger para atualizar serviços via SSH ou push para registry.

## 🛡️ Checklist de Segurança de Produção

- [ ] `DEBUG` desativado.
- [ ] `ALLOWED_HOSTS` configurado com o domínio real.
- [ ] Senhas de banco e chaves JWT únicas e complexas.
- [ ] Volume de `staticfiles` e `mediafiles` montado corretamente no Nginx.
- [ ] Sentry DSN configurado para alerta de erros.

## 📁 Gestão de Arquivos e Armazenamento

- **Static**: Coletados via `python manage.py collectstatic` no build.
- **Media**: Armazenados no volume `media_volume`. O sistema gera relatórios PDF e CSV que ficam disponíveis para download do usuário por este volume.
- **Backup**: Recomenda-se o backup periódico do volume `postgres_data_prod`.
