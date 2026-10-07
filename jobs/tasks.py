from celery import shared_task
from .services.hh_parser import fetch_hh_vacancies
from .services.habr_parser import fetch_habr_vacancies


@shared_task
def update_vacancies_task():
    """Фоновый сбор вакансий со всех доступных платформ"""
    # 1. HeadHunter
    try:
        fetch_hh_vacancies("python backend")
        fetch_hh_vacancies("Backend-developer")
        fetch_hh_vacancies("Backend-разработчик")
        fetch_hh_vacancies("Backend разработчик")
        fetch_hh_vacancies("Python-разработчик")
    except Exception as e:
        print(f"Ошибка сбора с HH: {e}")

    # 2. Habr карьера
    try:
        fetch_habr_vacancies("python")
        fetch_habr_vacancies("Backend-developer")
        fetch_habr_vacancies("Backend-разработчик")
        fetch_habr_vacancies("Backend разработчик")
        fetch_habr_vacancies("Python-разработчик")
    except Exception as e:
        print(f"Ошибка сбора с Habr: {e}")

    # 3. SuperJob
    try:
        fetch_superjob_vacancies("Python")
        fetch_superjob_vacancies("Backend-developer")
        fetch_superjob_vacancies("Backend-разработчик")
        fetch_superjob_vacancies("Backend разработчик")
        fetch_superjob_vacancies("Python-разработчик")
    except Exception as e:
        print(f"Ошибка сбора с SuperJob: {e}")

    return "Агрегация завершена."
