# -*- coding:utf-8 -*-

from django.db import models


class User(models.Model):
    bduss = models.CharField(max_length=192, verbose_name="BDUSS")
    username = models.CharField(max_length=30, unique=True, editable=False, verbose_name="贴吧用户名")
    token = models.CharField(max_length=200, unique=True, editable=False, verbose_name="个人TOKEN")
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="提交时间")
    flag = models.IntegerField(null=True, default=0, verbose_name="新用户")  # 默认0 已update1 已sign2

    def __str__(self):
        return self.username

    @property
    def all_bind(self):
        return self.sign_set.all().count()

    @property
    def signed(self):
        return self.sign_set.all().filter(is_sign=1).count()

    @property
    def unsigned(self):
        return self.sign_set.all().filter(is_sign=0).count()

    class Mete:
        get_latest_by = "created_time"
        table_name = 'user'
        ordering = ['created_time']
        verbose_name = r"用户"
        verbose_name_plural = verbose_name


class Sign(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    fid = models.CharField(max_length=20, verbose_name="贴吧id")
    is_sign = models.BooleanField(default=False, verbose_name="是否签到")
    ststus = models.CharField(max_length=100, verbose_name="签到状态")
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="所属用户")

    def __str__(self):
        return self.name

    class Mete:
        table_name = 'sign'
        verbose_name = '签到'
        verbose_name_plural = verbose_name

