from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('join', views.UserJoinView.as_view(), name='join'),
    path('isExist', views.UserIsExistView.as_view(), name='isExist'),
    path('logout', views.user_logout, name='logout'),
    path('update', views.user_update, name='update'),
    path('password', views.user_password, name='password'),
]
