from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'contas'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='contas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]
