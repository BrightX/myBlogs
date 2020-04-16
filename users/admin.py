from django.contrib import admin

from users.models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'gender')  # 添加字段显示
    search_fields = ('user', 'nickname', 'gender')  # 添加快速查询栏


admin.site.register(UserInfo, UserInfoAdmin)
