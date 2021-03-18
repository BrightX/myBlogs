from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    choices = (
        (True, '男'),
        (False, '女'),
    )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='用户')
    nickname = models.CharField(max_length=20, default='新用户', verbose_name='昵称')
    gender = models.BooleanField(choices=choices, default=True, verbose_name='性别')

    def __str__(self):
        return "%s : %s" % (self.user, self.nickname)

    class Meta:
        db_table = 't_userInfo'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
