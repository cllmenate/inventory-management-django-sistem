FROM nginx:1.27-alpine

# Set up directories and permissions for non-root execution
RUN apk add --no-cache curl && \
    mkdir -p /var/cache/nginx /var/run /run /var/log/nginx && \
    mkdir -p /var/lib/nginx/tmp/client_body /var/lib/nginx/tmp/proxy \
    /var/lib/nginx/tmp/fastcgi /var/lib/nginx/tmp/uwsgi /var/lib/nginx/tmp/scgi && \
    chown -R nginx:nginx /var/cache/nginx /var/run /run /var/log/nginx \
    /etc/nginx/conf.d /var/lib/nginx /usr/share/nginx/html && \
    sed -i 's/^user/#user/' /etc/nginx/nginx.conf && \
    sed -i 's|pid .*|pid /run/nginx.pid;|' /etc/nginx/nginx.conf && \
    rm /etc/nginx/conf.d/default.conf

# Copy custom configuration
COPY nginx.conf /etc/nginx/conf.d

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Use non-root user
USER nginx
