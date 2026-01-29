# Configuração do Sistema

Esta página documenta todas as variáveis de ambiente, configurações de segurança e diferenças entre ambientes de desenvolvimento e produção.

---

## 🔧 Variáveis de Ambiente

### Arquivo `.env`

O sistema utiliza um arquivo `.env` na raiz do projeto para configurações sensíveis. Use `.env.example` como template.

```bash
# Copiar template
cp .env.example .env
```

### Tabela Completa de Variáveis

| Variável | Tipo | Obrigatória | Padrão (Dev) | Descrição |
|----------|------|-------------|--------------|-----------|
| **Django Core** |
| `DEBUG` | Boolean | ✅ | `True` | Ativa modo de debug (⚠️ `False` em prod) |
| `SECRET_KEY` | String | ✅ | - | Chave de criptografia Django |
| `SIGNING_KEY` | String | ✅ | - | Chave de assinatura JWT |
| `ALLOWED_HOSTS` | String (CSV) | ✅ | `localhost,127.0.0.1` | Hosts permitidos |
| **Database** |
| `POSTGRES_DB` | String | ✅ | `inventory_db` | Nome do banco |
| `POSTGRES_USER` | String | ✅ | `inventory_user` | Usuário PostgreSQL |
| `POSTGRES_PASSWORD` | String | ✅ | - | Senha do banco |
| `POSTGRES_HOST` | String | ✅ | `inventory_db` | Host do PostgreSQL |
| `POSTGRES_PORT` | Integer | ✅ | `5432` | Porta do PostgreSQL |
| **Redis** |
| `REDIS_HOST` | String | ✅ | `inventory_redis` | Host do Redis |
| `REDIS_PORT` | Integer | ✅ | `6379` | Porta do Redis |
| `REDIS_DB` | Integer | ❌ | `0` | Índice do banco Redis |
| **Celery** |
| `CELERY_BROKER_URL` | String | ✅ | `redis://inventory_redis:6379/0` | URL do broker |
| `CELERY_RESULT_BACKEND` | String | ❌ | `django-db` | Backend de resultados |
| **Sentry** |
| `SENTRY_DSN` | String | ❌ | - | DSN do Sentry (monitoramento) |
| `SENTRY_ENVIRONMENT` | String | ❌ | `development` | Ambiente (`dev`, `prod`) |
| **CORS** |
| `CORS_ALLOWED_ORIGINS` | String (CSV) | ❌ | `http://localhost:3000` | Origins permitidas |

---

## 🔐 Segurança: Geração de Chaves

### SECRET_KEY

```python
# Gerar nova chave Django
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### SIGNING_KEY (JWT)

```python
# Gerar chave forte para JWT
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

> **IMPORTANTE**: Use chaves **diferentes** para `SECRET_KEY` e `SIGNING_KEY`.

---

## 🌍 Ambientes: Dev vs Prod

### Desenvolvimento (docker-compose.yml)

```yaml
services:
  inventory_web:
    environment:
      - DEBUG=True
      - ALLOWED_HOSTS=localhost,127.0.0.1
      - SENTRY_ENVIRONMENT=development
    command: python manage.py runserver 0.0.0.0:8000
```

**Características**:
- Hot reload (código atualiza automaticamente)
- Debug toolbar ativado
- Logs verbosos no console
- SQLite para testes (via pytest)

### Produção (docker-compose.prod.yml)

```yaml
services:
  inventory_web:
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
      - SENTRY_ENVIRONMENT=production
    command: gunicorn app.wsgi:application --bind 0.0.0.0:8000
```

**Características**:
- `DEBUG=False` (obrigatório)
- Gunicorn com múltiplos workers
- Logs enviados para Sentry
- HTTPS obrigatório (Nginx)

---

## 📊 Configuração de Cache (Redis)

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'inventory',
        'TIMEOUT': 300,  # 5 minutos padrão
    }
}
```

### Uso no código

```python
from django.core.cache import cache

# Salvar
cache.set('metrics:product', data, timeout=600)

# Ler
data = cache.get('metrics:product')
```

---

## 🔒 Configuração de CORS

Para permitir que frontends externos acessem a API:

```python
# .env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://app.seudominio.com

# settings.py (já configurado)
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
```

---

## 📧 Configuração de Email (Futuro)

```python
# Para notificações por email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
```

---

## 🛡️ Checklist de Segurança para Produção

- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` configurado com domínio real
- [ ] `SECRET_KEY` única e complexa (mínimo 50 caracteres)
- [ ] `SIGNING_KEY` diferente de `SECRET_KEY`
- [ ] Senha do PostgreSQL forte (mínimo 16 caracteres)
- [ ] Sentry DSN configurado para monitoramento
- [ ] HTTPS configurado no Nginx
- [ ] Firewall bloqueando portas 5432, 6379 (apenas Docker interno)
- [ ] Backup automático do volume `postgres_data_prod`
- [ ] Logs rotacionados (configurado no `docker-compose.prod.yml`)

---

## 🐳 Volumes Docker Persistentes

### Desenvolvimento

```yaml
volumes:
  postgres_data:  # Dados do banco
  redis_data:     # Dados do Redis
  media_volume:   # Arquivos de upload (exports)
```

### Produção

```yaml
volumes:
  postgres_data_prod:  # ⚠️ Fazer backup diário
  redis_data_prod:
  media_volume_prod:   # Relatórios gerados
```

---

## 🔍 Debugging de Configuração

### Verificar variáveis carregadas

```bash
# Dentro do container
docker exec -it inventory_web bash
python manage.py shell

>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.DATABASES)
```

### Testar conexão com PostgreSQL

```bash
docker exec -it inventory_db psql -U inventory_user -d inventory_db -c 'SELECT 1;'
```

### Testar conexão com Redis

```bash
docker exec -it inventory_redis redis-cli ping
# Resposta: PONG
```
