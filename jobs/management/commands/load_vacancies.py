from django.core.management.base import BaseCommand
from jobs.services.hh_parser import fetch_hh_vacancies
from jobs.services.superjob_parser import fetch_superjob_vacancies
from jobs.services.habr_parser import fetch_habr_vacancies


class Command(BaseCommand):
    help = 'Загружает свежие вакансии со всех источников'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='python backend')

    def handle(self, *args, **options):
        query = options['query']
        self.stdout.write(self.style.NOTICE(f'Сбор по запросу: "{query}"...'))

        fetch_hh_vacancies(text_query=query)
        fetch_superjob_vacancies(keyword=query)
        fetch_habr_vacancies(query="python")

        self.stdout.write(self.style.SUCCESS('Сбор успешно завершен!'))
