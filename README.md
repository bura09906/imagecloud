# ImageCloud
Приложение позволяет осуществлять работу с пользователем и его аватарами.
Загруженные изображения автоматически обрезаются до квадрата по центру, уменьшаются в размере и сохраняются в MinIO (локальное S3-хранилище).

## Стек технологий

- Python 3.12.8
- Django 4.2
- Django REST Framework
- Djoser (регистрация/логин/менеджмент пользователей)
- MinIO (через `django-storages` и `boto3`)
- Pillow (обработка изображений)
- PostgreSQL
- Celery
- Docker + Docker Compose

# Инструкция по развертыванию:
1. Клонировать репозиторий

2. Создать файл .env в корне проекта и добавьте туда:
   ```
    ACCESS_KEY_MINIO=minioadmin
    SECRET_KEY_MINIO=miniopassword

    POSTGRES_DB=imgcloude
    POSTGRES_USER=pg_user
    POSTGRES_PASSWORD=pg_password
    DB_HOST=db
    DB_PORT=5432
   ```
3. Выполнить команду для запуска контейнеров:
    ```
    docker compose up
    ```
4. Скопировать ваш .env в контейнер с django-приложением:
    ```
    docker cp .env img_cloud:/app/.env
    ```
5. Применить миграции:
    ```
    docker exec -it img_cloud python manage.py migrate
    ```
6. Запустить Celery через терминал в контейнере:
    ```
    docker exec -it img_cloud celery -A img_cloud worker --loglevel=info
    ```
7. Перейти в админ-зону MinIO, залогинится, создать Bucket
    http://127.0.0.1:9001
    username, password значения указзаные вами в .env
    название Bucket = imgcloud
8. При получении ссылки на изображение объекта Avatar через Postman, что бы получить само изображение необходимо указать AuthType = AWS Signature; AccessKey, SecretKey = значения указанные вами в .env; указать Service Name = s3