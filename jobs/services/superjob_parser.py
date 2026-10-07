import requests
from datetime import datetime, timezone
from django.conf import settings
from jobs.models import Vacancy


def fetch_superjob_vacancies(keyword="Python"):
    api_key = settings.SUPERJOB_API_KEY
    if not api_key:
        print("⚠️ SUPERJOB_API_KEY не задан в .env")
        return

    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": api_key,
        "User-Agent": "JobAggregator/1.0"
    }
    params = {
        "keyword": keyword,
        "count": 40,       # Количество вакансий на страницу
        "no_agreement": 0  # 0 — включая вакансии без указания ЗП
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            print(f"❌ Ошибка SuperJob API: {response.status_code}")
            return

        data = response.json()
        objects = data.get('objects', [])
        saved_count = 0

        for item in objects:
            # 1. Формат работы (у SuperJob: type_of_work -> id: 6 — удаленная работа)
            type_of_work_id = item.get('type_of_work', {}).get('id')
            work_format = 'remote' if type_of_work_id == 6 else 'office'

            # 2. Зарплата (0 означает "не указана")
            payment_from = item.get('payment_from') or None
            payment_to = item.get('payment_to') or None
            if payment_from == 0:
                payment_from = None
            if payment_to == 0:
                payment_to = None

            # Получаем timestamp публикации
            ts = item.get('date_published')

            if ts:
                # Преобразуем timestamp с явным указанием UTC
                date_published = datetime.fromtimestamp(ts, tz=timezone.utc)
            else:
                # Если дата не пришла, ставим текущее время
                date_published = datetime.now(tz=timezone.utc)

            # 4. Описание
            description = item.get('candidat') or "Описание доступно по ссылке."

            Vacancy.objects.update_or_create(
                external_url=item['link'],
                defaults={
                    'title': item['profession'],
                    'company': item.get('firm_name') or 'Компания не указана',
                    'sphere': item.get('client', {}).get('profession') or 'IT',
                    'description': description[:3000],
                    'work_format': work_format,
                    'salary_from': payment_from,
                    'salary_to': payment_to,
                    'source': 'SuperJob',
                    'published_at': date_published,
                }
            )
            saved_count += 1

        print(f"✅ SuperJob: успешно загружено {saved_count} вакансий.")

    except requests.RequestException as e:
        print(f"⚠️ Ошибка сети при обращении к SuperJob: {e}")
