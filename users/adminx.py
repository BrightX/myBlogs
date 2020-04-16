import xadmin
from .models import UserInfo


class UserInfoAdmin:
    list_display = ('user', 'nickname', 'gender')  # 添加字段显示
    search_fields = ('user', 'nickname', 'gender')  # 添加快速查询栏


xadmin.site.register(UserInfo, UserInfoAdmin)
