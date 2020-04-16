from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    path('<int:user_id>/', views.author, name='author'),
    path('<int:user_id>/<int:blog_id>.html', views.detail, name='detail'),
    path('create_blog', views.blog_create, name='blog_create'),

    # tag(标签)的增删改查
    path('tagCreate/<str:name>', views.tag_create, name='tag_create'),
    path('tagDelete/<int:tag_id>', views.tag_delete, name='tag_delete'),
    path('tagUpdate/<int:tag_id>/<str:name>', views.tag_update, name='tag_update'),
    path('tagIsExist/<str:name>', views.tag_is_exist, name='tag_is_exist'),

]
