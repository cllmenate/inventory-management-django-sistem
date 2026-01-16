#!/bin/sh

# Verifica se o serviço é postgres e aguarda
if [ "$DATABASE" = "postgres" ]
then
    echo "Aguardando PostgreSQL..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL iniciado"
fi

exec "$@"