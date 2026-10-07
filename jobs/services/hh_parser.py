import random
from django.utils import timezone
from jobs.models import Vacancy
from datetime import timedelta


def fetch_hh_vacancies(text_query="python backend"):
    print(f"Генерируем 20 новых вакансий по запросу '{text_query}'...")

    companies = ["Яндекс", "VK", "Avito", "Tinkoff", "Сбер", "Ozon", "Крутой Стартап", "ТехноПарк"]
    formats = ["remote", "office", "hybrid"]
    levels = ["Junior", "Middle", "Senior", "Lead"]

    saved_count = 0
    for i in range(20):
        # Генерируем уникальный ID для каждой из 20 вакансий
        fake_id = random.randint(90000000, 99999999)
        lvl = random.choice(levels)

        Vacancy.objects.create(
            title=f"{lvl} {text_query.title()} Developer",
            company=random.choice(companies),
            sphere='IT',
            description=f"Мы ищем {lvl} специалиста. Нужно писать чистый код на Python, работать с базами данных и не бояться Docker. Отличный коллектив!",
            work_format=random.choice(formats),
            salary_from=random.randint(80, 150) * 1000,
            salary_to=random.randint(160, 350) * 1000,
            source='Mock Generator',
            external_url=f"https://hh.ru/vacancy/{fake_id}",
            published_at=timezone.now() - timedelta(hours=random.randint(1, 72))
        )
        saved_count += 1

    print(f"✅ Успешно сгенерировано {saved_count} тестовых вакансий!")
