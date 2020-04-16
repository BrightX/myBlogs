from django.contrib.auth.models import Group, User
from guardian.shortcuts import assign_perm


def get_or_create_author_group():
    """
    返回`作者`用户组并设置基本权限
    """
    name = '作者'
    if Group.objects.filter(name=name).exists():
        group = Group.objects.get(name=name)
    else:
        group = Group.objects.create(name=name)

    perms = (
        'blogs.add_tag',
        'blogs.add_article',
        'blogs.add_comment',
        'blogs.add_category',
        'blogs.view_tag',
        'blogs.view_article',
        'blogs.view_comment',
        'blogs.view_category',
    )
    for perm in perms:
        assign_perm(perm, group)
    return group


def user_perm_init(user: User):
    """为普通用户添加基本权限"""
    user_info = user.userinfo
    for perm in ('change_userinfo', 'view_userinfo'):
        assign_perm(perm, user, user_info)
    for perm in ('change_user', 'view_user'):
        assign_perm(perm, user, user)
