from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Vacancy, Application
from django.db.models import Count


def vacancy_list(request):
    """Главная страница: список вакансий с фильтрами"""
    vacancies = Vacancy.objects.all()

    # Обработка фильтров
    sphere = request.GET.get('sphere')
    work_format = request.GET.get('format')
    search_query = request.GET.get('q')

    if sphere:
        vacancies = vacancies.filter(sphere__icontains=sphere)
    if work_format:
        vacancies = vacancies.filter(work_format=work_format)
    if search_query:
        vacancies = vacancies.filter(title__icontains=search_query)

    return render(request, 'jobs/vacancy_list.html', {'vacancies': vacancies})


@login_required
def dashboard(request):
    """Личный кабинет пользователя со статистикой"""
    user = request.user
    today = timezone.now().date()

    # Временные рамки
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Статистика откликов
    applications = Application.objects.filter(user=user)

    stats = {
        'total': applications.count(),
        'today': applications.filter(applied_at__date=today).count(),
        'this_week': applications.filter(applied_at__date__gte=start_of_week).count(),
        'this_month': applications.filter(applied_at__date__gte=start_of_month).count(),
    }

    recent_applications = applications.select_related('vacancy').order_by('-applied_at')[:10]

    return render(request, 'jobs/dashboard.html', {
        'stats': stats,
        'recent_applications': recent_applications
    })


@login_required
def apply_vacancy(request, vacancy_id):
    """Ручка для отклика на вакансию"""
    if request.method == 'POST':
        vacancy = Vacancy.objects.get(id=vacancy_id)
        Application.objects.get_or_create(user=request.user, vacancy=vacancy)
    return redirect('dashboard')
