from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('join', views.user_join, name='join'),
    path('update', views.user_update, name='update'),
    path('password', views.user_password, name='password'),
    path('isExist', views.user_is_exist, name='isExist'),
]
