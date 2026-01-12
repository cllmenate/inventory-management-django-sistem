# syntax=docker/dockerfile:1
FROM astral/uv:python3.14-bookworm-slim

WORKDIR /inventory-management-django-system

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . .

RUN uv sync --frozen

ENV PATH="/inventory-management-django-system/.venv/bin:$PATH"

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]