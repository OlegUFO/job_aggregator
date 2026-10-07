import re
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from jobs.models import Vacancy


def parse_salary(salary_text):
    """
    Извлекает числа из строки вида:
    'от 150 000 до 250 000 ₽', 'от 180 000 ₽', 'до 300 000 ₽'
    """
    if not salary_text or 'договор' in salary_text.lower():
        return None, None

    # Очищаем от неразрывных пробелов
    clean_text = salary_text.replace('\xa0', ' ').replace(' ', '')

    sal_from = None
    sal_to = None

    from_match = re.search(r'от(\d+)', clean_text)
    to_match = re.search(r'до(\d+)', clean_text)

    if from_match:
        sal_from = int(from_match.group(1))
    if to_match:
        sal_to = int(to_match.group(1))

    return sal_from, sal_to


def fetch_habr_vacancies(query="python"):
    url = "https://career.habr.com/vacancies"
    params = {
        "q": query,
        "type": "all",
        "sort": "date"  # Сортировка по дате добавления
    }
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9",
    }

    print(f"Парсим Хабр Карьеру по запросу '{query}'...")

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Ошибка запроса к Хабр Карьере: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "lxml")
        vacancy_cards = soup.select(".vacancy-card")

        if not vacancy_cards:
            print("⚠️ Вакансии не найдены в разметке страницы.")
            return

        saved_count = 0

        for card in vacancy_cards:
            # 1. Ссылка и заголовок
            title_tag = card.select_one(".vacancy-card__title a")
            if not title_tag:
                continue

            relative_url = title_tag.get("href")
            external_url = f"https://career.habr.com{relative_url}"
            title = title_tag.get_text(strip=True)

            # 2. Компания
            company_tag = card.select_one(".vacancy-card__company-title a")
            company = company_tag.get_text(strip=True) if company_tag else "Компания не указана"

            # 3. Зарплата
            salary_tag = card.select_one(".basic-salary")
            salary_text = salary_tag.get_text(strip=True) if salary_tag else ""
            salary_from, salary_to = parse_salary(salary_text)

            # 4. Формат работы (удаленно, офис, гибрид)
            meta_tag = card.select_one(".vacancy-card__meta")
            meta_text = meta_tag.get_text(strip=True).lower() if meta_tag else ""

            work_format = "office"
            if "дистанционно" in meta_text or "удаленно" in meta_text:
                work_format = "remote"
            elif "гибрид" in meta_text:
                work_format = "hybrid"

            # 5. Краткое описание / стек навыков
            skills_tag = card.select_one(".vacancy-card__skills")
            skills = skills_tag.get_text(" • ", strip=True) if skills_tag else ""
            description = f"Требуемый стек: {skills}" if skills else "Подробности в описании вакансии."

            Vacancy.objects.update_or_create(
                external_url=external_url,
                defaults={
                    "title": title,
                    "company": company,
                    "sphere": "IT",
                    "description": description[:3000],
                    "work_format": work_format,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "source": "Habr Career",
                    "published_at": timezone.now(),
                }
            )
            saved_count += 1

        print(f"✅ Хабр Карьера: успешно сохранено/обновлено {saved_count} вакансий.")

    except requests.RequestException as e:
        print(f"⚠️ Ошибка сети при парсинге Хабра: {e}")
