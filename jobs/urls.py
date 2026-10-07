from django.urls import path
from . import views

urlpatterns = [
    # Главная страница (список вакансий)
    path('', views.vacancy_list, name='vacancy_list'),

    # Личный кабинет
    path('dashboard/', views.dashboard, name='dashboard'),

    # Скрытый URL для обработки нажатия на кнопку "Откликнуться"
    path('apply/<int:vacancy_id>/', views.apply_vacancy, name='apply_vacancy'),
]
