from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'mall'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.homepage, name='home'),
    path('cart/', views.cart, name='cart'),
    path('send_email/', views.send_email, name='send_email'),
    path('purchased/', views.purchased, name='purchased'),
    path('received/', views.received, name='received'),
    path('management/', views.management, name='management'),
    path('add_commodity/', views.add_commodity, name='add_commodity'),
    path('modify_commodity/<int:cd_id>', views.modify_commodity, name='modify_commodity'),
]
