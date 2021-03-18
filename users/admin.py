from django.contrib import admin

from users.models import UserInfo

admin.site.site_header = '站点后台管理'
admin.site.site_title = '站点后台'
admin.site.index_title = '后台管理'


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'gender')  # 添加字段显示
    search_fields = ('user', 'nickname', 'gender')  # 添加快速查询栏
