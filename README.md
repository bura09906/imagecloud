# ImageCloud
Приложение предназначено для загрузки, хранения и обработки изображений.
Загруженные изображения автоматически обрезаются до квадрата по центру, уменьшаются в размере и сохраняются в MinIO (локальное S3-хранилище).

## Стек технологий

- Python 3.12.8
- Django 4.2
- Django REST Framework
- MinIO (через `django-storages` и `boto3`)
- Pillow (обработка изображений)
- Docker + Docker Compose
- Pytest (тестирование)

# Инструкция по развертыванию:
1. Клонировать репозиторий
2. Создать и активировать виртуальное окружение:

   Команды для Windiws:
   ```
   python -m venv venv
   ```
   ```
   source venv/Scripts/activate
   ```
   Команды для Linux:
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ```
4. Установить зависимости из файла requirements.txt:
   ```
   pip install -r requirements.txt
   ```
5. Создать файл .env в корне проекта и добавьте туда:
   ```
   ACCESS_KEY_MINIO=minioadmin
   SECRET_KEY_MINIO=miniopassword
   ```
6. Запустить контейнер с MinIO:
    ```
    docker compose up
    ```
7. Перейти в админ-зону MinIO, залогинится, создать Bucket
    http://127.0.0.1:9001
    username, password значения указзаные вами в .env
    название Bucket = imgcloud
8. Применить миграции. Запустить сервер Django:
    ```
    python manage.py migrate

    python manage.py runserver
    ```

9. Тесты запускаются из корня проекта командой pytest
10. При получении ссылки на изображение объекта Avatar через Postman, что бы получить само изображение необходимо указать AuthType = AWS Signature; AccessKey, SecretKey = значения указанные вами в .env; указать Service Name = s3