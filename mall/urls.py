from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'mall'

urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('', views.index, name='index')
]
