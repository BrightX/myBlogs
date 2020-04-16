from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from blogs.models import Tag, Category, Article


def detail(request, user_id: int, blog_id: int) -> HttpResponse:
    """ TODO 博客详情页 Blog details page """
    if not Article.objects.filter(pk=blog_id).exists():
        return HttpResponse('404 NOT FOUND', status=404)

    article = Article.objects.get(pk=blog_id)
    context = {
        'blog': blog_id,
        'user_id': user_id,
        'blog_user': article.user,
        'title': article.title,
        'content': article.content,
        'create_time': article.create_time,
        'update_time': article.update_time,
    }
    return render(request, 'blogs/detail.html', context=context)


def author(request, user_id: int) -> HttpResponse:
    """ TODO 作者详情页 Author details page """
    context = {
        'author': user_id,
    }
    return render(request, 'blogs/author.html', context=context)


@login_required
def tag_create(request, name: str) -> JsonResponse:
    """ 添加新标签 """
    data = {
        'code': -1,
        'msg': 'error',
        'name': name,
    }
    if request.is_ajax():
        # 只接受Ajax请求
        data['msg'] = '该标签已存在'
        if not Tag.objects.filter(name=name).exists():
            # 如果已存在就不再添加标签
            data['code'] = 200
            data['msg'] = 'success'
            Tag.objects.create(name=name)
    return JsonResponse(data=data)


@login_required
def tag_delete(request, tag_id: int) -> JsonResponse:
    """ 删除标签 """
    data = {
        'code': -1,
        'msg': 'error',
        'tag_id': tag_id,
    }
    if not request.is_ajax():
        # 只接受Ajax请求
        return JsonResponse(data=data)

    if not Tag.objects.filter(id=tag_id).exists():
        # 如果数据不存在，就不执行删除操作
        data['msg'] = 'does not exist'
        return JsonResponse(data=data)

    tag = Tag.objects.get(id=tag_id)
    data['code'] = 200
    data['msg'] = 'success'
    data['tag'] = tag.name
    tag.delete()
    return JsonResponse(data=data)


@login_required
def tag_update(request, tag_id: int, name: str) -> JsonResponse:
    """ 修改标签 """
    data = {
        'code': -1,
        'msg': 'error',
        'tag_id': tag_id,
        'new_name': name,
    }
    if not request.is_ajax():
        # 只接受Ajax请求
        return JsonResponse(data=data)

    if not Tag.objects.filter(id=tag_id).exists():
        # 如果不存在，就不执行修改
        data['msg'] = 'does not exist'
        return JsonResponse(data=data)

    tag = Tag.objects.get(id=tag_id)
    data['code'] = 200
    data['msg'] = 'success'
    data['old_name'] = tag.name
    tag.name = name
    return JsonResponse(data=data)


@login_required
def tag_is_exist(request, name: str) -> JsonResponse:
    """ 查询标签名是否已存在 """
    data = {
        'code': 200,
        'isExist': False,
        'name': name,
    }
    if Tag.objects.filter(name=name).exists():
        data['isExist'] = True
        data['tag_id'] = Tag.objects.get(name=name).id
        return JsonResponse(data=data)
    return JsonResponse(data)


@login_required
def category_create(request) -> [HttpResponse, JsonResponse]:
    """ TODO 创建文章分类 """
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        info = request.POST.get('info')
        data = {
            'code': 200,
            'msg': 'success'
        }
        try:
            category = Category.objects.create(user=user, name=name)
            if info:
                category.info = info
            category.save()
        except Exception as e:
            data['code'] = -1
            data['msg'] = 'error'
            print(e)  # FIXME 异常处理待优化
        return JsonResponse(data=data)
    if request.method == 'GET':
        return render(request, 'blogs/category_create.html')
    return HttpResponse("404 NOT FOUND", status=404)


@login_required
def category_update(request) -> (HttpResponse, JsonResponse):
    """ TODO 编辑文章分类 """
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        info = request.POST.get('info')
        data = {
            'code': 200,
            'msg': 'success'
        }
        try:
            category = Category.objects.get(user=user, name=name)
            if info:
                category.info = info
            category.save()
        except Exception as e:
            data['code'] = -1
            data['msg'] = 'error'
            print(e)  # FIXME 异常处理待优化
        return JsonResponse(data=data)
    if request.method == 'GET':
        return render(request, 'blogs/category_create.html')
    return HttpResponse("404 NOT FOUND", status=404)


def blog_create(request):
    """ TODO 添加博客 """
    if request.method == 'GET':
        return render(request, 'blogs/blog_create.html')
    if request.method == 'POST':
        pass
    return HttpResponse("404 NOT FOUND", status=404)
