from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/index.html'), name='logout'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
]