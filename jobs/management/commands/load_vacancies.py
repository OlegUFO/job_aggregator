from django.core.management.base import BaseCommand
from jobs.services.hh_parser import fetch_hh_vacancies
from jobs.models import Vacancy


class Command(BaseCommand):
    help = 'Загружает свежие вакансии с HH.ru в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='python backend')

    def handle(self, *args, **options):
        query = options['query']

        # ОЧИЩАЕМ БАЗУ ОТ СТАРЫХ ВАКАНСИЙ ПЕРЕД ГЕНЕРАЦИЕЙ
        deleted_count, _ = Vacancy.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Удалено старых вакансий: {deleted_count}'))

        self.stdout.write(self.style.NOTICE(f'Начинаем сбор вакансий по запросу: "{query}"...'))
        try:
            fetch_hh_vacancies(text_query=query)
            self.stdout.write(self.style.SUCCESS('Команда успешно завершена!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))