from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    """ 文章标签 """
    name = models.CharField(max_length=15, unique=True, verbose_name='文章标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """ 文章分类 """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='作者')
    name = models.CharField(max_length=20, verbose_name='文章分类')
    info = models.CharField(max_length=255, null=True, verbose_name='分类简介')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='分类创建时间')

    def __str__(self):
        return "%s: %s" % (self.name, self.user.username)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """ 文章内容 """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='文章作者')
    title = models.CharField(max_length=100, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    tags = models.ManyToManyField(to=Tag, verbose_name='文章标签')
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, null=True, verbose_name='文章分类')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='文章创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='文章修改时间')

    def __str__(self):
        return "%s: %s" % (self.user.username, self.title)

    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name


class ArticlePlus(models.Model):
    """ 文章附加信息 """
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='文章内容')
    page_view = models.BigIntegerField(default=0, verbose_name='浏览量')
    thumb = models.BigIntegerField(default=0, verbose_name='点赞量')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = '文章附加信息'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """ 文章评论与回复 """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, null=True, blank=True, verbose_name='评论的文章')
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='回复的评论')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='文章创建时间')

    def __str__(self):
        return "%s: %s" % (self.user.username, self.content[:20])

    class Meta:
        verbose_name = '文章评论与回复'
        verbose_name_plural = verbose_name
