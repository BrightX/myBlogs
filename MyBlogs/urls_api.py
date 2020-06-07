from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('blogs/', include("blogs.urls")),
    path('uesrs/', include("users.urls")),
]
