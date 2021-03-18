from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserInfo
from users.utils import get_or_create_author_group, user_perm_init


class UserLoginView(TemplateView):
    """用户登录视图"""
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '/')

        if request.user.is_authenticated:
            """若用户已登录，则跳过登录界面"""
            return redirect(next_url)

        captcha_hashkey = CaptchaStore.generate_key()  # 生成验证码的hashkey
        captcha_img_url = captcha_image_url(captcha_hashkey)  # 生成验证码图片
        self.extra_context = {
            'captcha_hashkey': captcha_hashkey,
            'captcha_img_url': captcha_img_url,
            'next': next_url,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        next_url = self.request.GET.get('next') or self.request.POST.get('next', '/')
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        hashkey = request.POST.get('captcha_0')
        captcha = request.POST.get('captcha_1').strip()

        data = {
            'code': -1,
            'msg': 'error',
            'next': next_url,
        }

        captcha_store = CaptchaStore.objects.filter(hashkey=hashkey).first()
        if not captcha_store or captcha_store.response != captcha.lower():
            data['msg'] = '验证码错误'
            return JsonResponse(data)

        if not username or not password:
            data['msg'] = '用户名或密码不能为空'
            return JsonResponse(data)

        user = auth.authenticate(username=username, password=password)
        if not user:
            data['msg'] = '用户名或密码错误'
            return JsonResponse(data)

        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        data['code'] = 200
        data['msg'] = "登录成功"
        return JsonResponse(data)


class UserJoinView(TemplateView):
    """用户注册视图"""
    template_name = 'users/join.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '/')
        if request.user.is_authenticated:
            """若用户已登录，则跳过注册界面"""
            return redirect(next_url)

        captcha_hashkey = CaptchaStore.generate_key()
        captcha_img_url = captcha_image_url(captcha_hashkey)
        self.extra_context = {
            'captcha_hashkey': captcha_hashkey,
            'captcha_img_url': captcha_img_url,
            'next': next_url,
        }
        return super(UserJoinView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        next_url = self.request.GET.get('next') or self.request.POST.get('next', '/')
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        hashkey = request.POST.get('captcha_0', 'error')
        captcha = request.POST.get('captcha_1', 'error_1').strip()
        nickname = request.POST.get('nickname', '新用户')
        gender = request.POST.get('gender')

        data = {
            'code': -1,
            'next': next_url,
            'msg': 'error',
        }

        captcha_store = CaptchaStore.objects.filter(hashkey=hashkey).first()
        if not captcha_store or captcha_store.response != captcha.lower():
            data['msg'] = '验证码错误'
            return JsonResponse(data=data)

        if not username or not password:
            data['msg'] = '用户名或密码不能为空'
            return JsonResponse(data)

        if User.objects.filter(username=username).exists():
            data['msg'] = '该用户名已存在'
            return JsonResponse(data)

        user = User.objects.create_user(username=username, password=password)
        group = get_or_create_author_group()
        user.groups.add(group)
        user_info = UserInfo.objects.create(user=user)
        user_perm_init(user)
        if nickname:
            user_info.nickname = nickname.strip()
        if gender is not None:
            user_info.gender = bool(int(gender))
        user_info.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        data['code'] = 200
        data['msg'] = "注册成功"
        return JsonResponse(data)


class UserIsExistView(APIView):
    """ 查询用户是否已存在 """

    def get(self, *args, **kwargs):
        username = self.request.query_params.get('username')
        data = {
            'code': 200,
            'isExist': False,
            'username': username,
        }
        if username:
            data['isExist'] = User.objects.filter(username=username).exists()
        return Response(data)


@login_required
def user_logout(request):
    """ 退出登录 """
    auth.logout(request)
    return redirect("users:login")


@login_required
def user_update(request) -> (HttpResponse, JsonResponse):
    """TODO 修改用户信息"""
    if request.method == "GET":
        return render(request, "users/update.html")

    if request.method == "POST":
        user = request.user
        data = {
            'code': -1,
            'msg': 'error',
            'username': user.username
        }

        if request.is_ajax() or True:  # FIXME 测试 需要删掉 ` or True`
            nickname = request.POST.get('nickname')
            gender = request.POST.get('gender')
            if nickname:
                user.userinfo.nickname = nickname
            if gender is not None:
                user.userinfo.gender = bool(int(gender))
            user.userinfo.save()
            data['code'] = 200
            data['msg'] = '修改成功'
            data['next'] = reverse("users:update")
            return JsonResponse(data=data)

    return HttpResponse("403 禁止访问", status=403)


@login_required
def user_password(request) -> (HttpResponse, JsonResponse):
    """
    修改用户密码
    只接受Ajax的POST请求
    """
    if request.method == "GET":
        return redirect('users:update')
    user = request.user
    if request.method == "POST" and user.has_perm('change_user', user):
        if request.is_ajax() or True:  # FIXME 测试 需要删掉 ` or True`
            data = {
                'code': -1,
                'msg': 'error',
                'username': user.username,
            }
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')

            if old_password and new_password:
                if not user.check_password(old_password):
                    data['msg'] = '密码错误'
                    return JsonResponse(data=data)

                user.set_password(new_password)
                user.save()
                data['code'] = 200
                data['msg'] = '密码修改成功，请重新登录'
                data['next'] = reverse('users:login')
            return JsonResponse(data=data)

    return HttpResponse("403 禁止访问", status=403)
