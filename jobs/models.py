from django.db import models
from django.contrib.auth.models import User

class Vacancy(models.Model):
    WORK_FORMATS = (
        ('remote', 'Удаленно'),
        ('office', 'Очно'),
        ('hybrid', 'Гибрид'),
    )

    title = models.CharField('Должность', max_length=255)
    company = models.CharField('Компания', max_length=255)
    sphere = models.CharField('Сфера деятельности', max_length=255, db_index=True)
    description = models.TextField('Описание')
    work_format = models.CharField('Формат работы', max_length=20, choices=WORK_FORMATS)
    salary_from = models.IntegerField('ЗП от', null=True, blank=True)
    salary_to = models.IntegerField('ЗП до', null=True, blank=True)
    source = models.CharField('Источник (HH, Habr, TG)', max_length=50)
    external_url = models.URLField('Ссылка на вакансию', unique=True)
    published_at = models.DateTimeField('Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} - {self.company}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    applied_at = models.DateTimeField('Дата отклика', auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vacancy')
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'