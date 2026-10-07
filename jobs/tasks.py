from celery import shared_task
from .services.hh_parser import fetch_hh_vacancies

@shared_task
def update_vacancies_task():
    """Фоновая задача для обновления вакансий"""
    fetch_hh_vacancies("python backend")
    fetch_hh_vacancies("Backend-developer")
    fetch_hh_vacancies("Backend-разработчик")
    fetch_hh_vacancies("Backend разработчик")
    fetch_hh_vacancies("Python-разработчик")
    # В будущем сюда добавишь fetch_tg_vacancies(), fetch_habr_vacancies() и т.д.
    return "Сбор вакансий завершен!"

