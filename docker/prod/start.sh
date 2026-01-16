#!/bin/sh
# Roda migrações (opcional aqui, idealmente roda no CI/CD)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Exporta PYTHONPATH para garantir que o pacote app seja encontrado
export PYTHONPATH=$PYTHONPATH:/inventory-management-django-system

# Inicia o servidor apropriado dependendo do ambiente
if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "1" ]; then
    echo "Iniciando em modo de DESENVOLVIMENTO (runserver)..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Iniciando em modo de PRODUÇÃO (Gunicorn)..."
    python manage.py collectstatic --noinput
    exec gunicorn --bind 0.0.0.0:8000 \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --log-level info \
        app.asgi:application
fi