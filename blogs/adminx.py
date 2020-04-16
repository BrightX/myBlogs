import xadmin
from xadmin import views

from blogs.models import Article, Tag, Category, Comment
from users.models import UserInfo


class ArticleAdmin:
    list_display = ('id', 'user', 'title', 'category', 'create_time', 'update_time')  # 文章列表里显示想要显示的字段
    list_per_page = 50  # 满50条数据就自动分页
    ordering = ('-create_time',)  # 后台数据列表排序方式
    list_display_links = ('id', 'title')  # 设置哪些字段可以点击进入编辑界面


class TagAdmin:
    list_display = ('id', 'name')
    list_per_page = 50
    list_display_links = ('id', 'name')


class CategoryAdmin:
    list_display = ('id', 'user', 'name', 'create_time')
    list_per_page = 50
    list_display_links = ('id', 'name')


class CommentAdmin:
    list_display = ('id', 'user', 'article', 'parent', 'create_time')
    list_per_page = 50
    list_display_links = ('id', 'user', 'article', 'parent')


class GlobalSetting(object):
    """全局设置，最好放到adminx.py开头位置 """

    # 设置base_site.html的Title
    site_title = 'MyBlogs后台管理'
    # 设置base_site.html的Footer
    site_footer = 'MyBlogs'
    menu_style = "accordion"  # 菜单折叠

    global_models_icon = {
        UserInfo: "glyphicon glyphicon-user",
        Article: "fa fa-file-text",
        Tag: "glyphicon glyphicon-tags",
        Category: "fa fa-certificate",
        Comment: "glyphicon glyphicon-comment",
    }  # 设置models的全局图标
    # http://www.wapadd.cn/icons/awesome/index.htm
    # https://v3.bootcss.com/components/


class ThemeSetting(object):
    """主题设置"""
    enable_themes = True  # 使用主题
    use_bootswatch = True  # bootswatch是一款基于bootstrap的汇集了多种风格的前端UI解决方案


xadmin.site.register(views.BaseAdminView, ThemeSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Comment, CommentAdmin)
