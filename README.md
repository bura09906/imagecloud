#ImageCloud
Приложение предназначено для загрузки, хранения и обработки изображений.
Загруженные изображения автоматически обрезаются до квадрата по центру, уменьшаются в размере и сохраняются в MinIO (локальное S3-хранилище).

##Стек технологий

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
5. Создаnm файл .env в корне проекта и добавьте туда:
   
