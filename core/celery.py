import os
from celery import Celery

# Задаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создаем экземпляр Celery
app = Celery('core')

# Загружаем настройки из settings.py, все переменные Celery должны начинаться с CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи (tasks.py) в наших приложениях (jobs)
app.autodiscover_tasks()