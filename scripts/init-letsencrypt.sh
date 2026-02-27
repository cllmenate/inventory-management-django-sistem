#!/bin/bash

# Este script inicializa os certificados Let's Encrypt para que o Nginx consiga subir pela primeira vez.
# Adaptação do script famoso do wmnnd/nginx-certbot.

if ! [ -x "$(command -v docker)" ]; then
  echo 'Erro: docker não está instalado.' >&2
  exit 1
fi

if ! [ -x "$(command -v docker compose)" ]; then
  echo 'Erro: docker compose (v2) não está instalado.' >&2
  exit 1
fi

domains=(seusubdominio.com.br www.seusubdominio.com.br)
rsa_key_size=4096
data_path="./certbot"
email="seuemail@exemplo.com" # Adicione um email válido
staging=0 # Mude para 1 se estiver testando para evitar limite de requisições da Let's Encrypt

if [ -d "$data_path" ]; then
  read -p "Dados existentes encontrados de uma certificação anterior. Substituir e renovar? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi

if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Baixando parâmetros TLS recomendados ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

echo "### Criando certificado dummy para $domains ..."
path="/etc/letsencrypt/live/$domains"
mkdir -p "$data_path/conf/live/$domains"
docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

echo "### Iniciando Nginx ..."
docker compose -f docker-compose.prod.yml up --force-recreate -d inventory_nginx
echo

echo "### Deletando certificado dummy para $domains ..."
docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$domains && \
  rm -Rf /etc/letsencrypt/archive/$domains && \
  rm -Rf /etc/letsencrypt/renewal/$domains.conf" certbot
echo

echo "### Solicitando certificado Let's Encrypt para $domains ..."
# Junta os dominios na flag -d
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Configura o email
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Ativa o modo staging se for teste
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker compose -f docker-compose.prod.yml run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo

echo "### Reiniciando Nginx ..."
docker compose -f docker-compose.prod.yml exec inventory_nginx nginx -s reload
