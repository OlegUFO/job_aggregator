from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Подключаем маршруты нашего приложения
    path('', include('jobs.urls')),
    
    # Подключаем стандартные вьюхи Django для авторизации
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
