"""MyBlogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from django.views.static import serve

from MyBlogs.settings import MEDIA_ROOT

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html', content_type='text/html')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('admin/', admin.site.urls),
    path('blog/', include('blogs.urls')),
    path('captcha/', include('captcha.urls')),  # 图片验证码路由
    path('user/', include('users.urls')),
    path('user/', include('users.urls.password_url')),
    path("media/<path:path>", serve, {"document_root": MEDIA_ROOT}),

    re_path(r'^api/(?P<version>v\d+)/', include("MyBlogs.urls_api")),
]
