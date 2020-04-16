from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from blogs.models import Article, Tag, Category, Comment


@admin.register(Article)
class ArticleAdmin(GuardedModelAdmin):
    list_display = ('id', 'user', 'title', 'category', 'create_time', 'update_time')  # 文章列表里显示想要显示的字段
    list_per_page = 50  # 满50条数据就自动分页
    ordering = ('-create_time',)  # 后台数据列表排序方式
    list_display_links = ('id', 'title')  # 设置哪些字段可以点击进入编辑界面


@admin.register(Tag)
class TagAdmin(GuardedModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 50
    list_display_links = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(GuardedModelAdmin):
    list_display = ('id', 'user', 'name', 'create_time')
    list_per_page = 50
    list_display_links = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(GuardedModelAdmin):
    list_display = ('id', 'user', 'article', 'parent', 'create_time')
    list_per_page = 50
    list_display_links = ('id', 'user', 'article', 'parent')
