from celery import shared_task
from django.core.files.storage import default_storage


@shared_task
def delete_image_s3(file_path):
    print('Запуск задачи')
    if default_storage.exists(file_path):
        default_storage.delete(file_path)
        print(f'Файл {file_path} удалён из хранилища')
    else:
        print(f'Файл {file_path} не найден в хранилище')
