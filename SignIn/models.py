# -*- coding:utf-8 -*-
import time
import uuid

from django.db import models

from SignIn.utils import utils


class UserManager(models.Manager):

    def new(self, bduss):
        name = utils.get_name(bduss)
        print(name)
        token = str(uuid.uuid1())
        obj, created = User.objects.update_or_create(username=name, defaults={"bduss": bduss, "token": token})
        return created

    def need_update_like(self):
        return User.objects.filter(flag=0)

    def set_status_liking(self):
        User.objects.filter(flag=0).update(flag=1)


class User(models.Model):
    bduss = models.CharField(max_length=192, verbose_name="BDUSS")
    username = models.CharField(max_length=30, unique=True, editable=False, verbose_name="贴吧用户名")
    token = models.CharField(max_length=200, unique=True, editable=False, verbose_name="个人TOKEN")
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="提交时间")
    flag = models.IntegerField(null=True, default=0, verbose_name="新用户")  # 默认0 已update1
    objects = UserManager()

    def __str__(self):
        return self.username

    def like(self):
        res = utils.get_favorite(self.bduss)
        return res

    def like_callback(self, res):
        res = res.result()
        for i in res:
            print(time.time(), "获取到新关注的贴吧:", i["name"])
            Sign.objects.get_or_create(fid=i["id"], name=i["name"], user=self,
                                       defaults={"fid": i["id"], "name": i["name"], "user": self})

    class Meta:
        get_latest_by = "created_time"
        db_table = 'user'
        ordering = ['created_time']
        verbose_name = r"用户"
        verbose_name_plural = verbose_name


class SignManager(models.Manager):

    def need_sign(self):
        obj = Sign.objects.filter(is_sign=False)
        return obj

    def set_status_signing(self):
        Sign.objects.filter(is_sign=False).update(is_sign=True)


class Sign(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    fid = models.CharField(max_length=20, verbose_name="贴吧id")
    is_sign = models.BooleanField(default=False, verbose_name="是否签到")
    ststus = models.CharField(max_length=100, verbose_name="签到状态", default="")
    retry_times = models.SmallIntegerField(verbose_name="重试次数", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")
    objects = SignManager()

    def __str__(self):
        return self.name

    def sign(self):
        print(time.time(), "签到贴吧：", self.name)
        res = utils.client_sign(bduss=self.user.bduss, sign=self)
        return {"res": res, 'sign': self}

    def sign_callback(self, res):
        result = res.result()
        res = result["res"]
        sign = result["sign"]
        # 日志记录
        SignLog.objects.log(sign, res)
        # 签到状态判断
        if res['error_code'] != 0:
            self.is_sign = False
            self.retry_times += 1
        # 如果尝试签到5次还未成功，则不再尝试
        # todo: 修改最大尝试次数
        if self.retry_times == 2:
            self.is_sign = True
        self.ststus = res['error_msg']
        self.save()

    class Meta:
        db_table = 'sign'
        verbose_name = '签到'
        verbose_name_plural = verbose_name
        unique_together = (('name', 'fid', 'user'),)


class SignLogManager(models.Manager):

    @staticmethod
    def log(sign, ret_log):
        log_obj = SignLog(name=sign.name, user=sign.user, ret_log=ret_log)
        log_obj.save()


class SignLog(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="提交时间")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")
    ret_log = models.TextField(verbose_name="签到日志")
    objects = SignLogManager()

    class Meta:
        db_table = 'sign_log'
        verbose_name = '签到日志'
        verbose_name_plural = verbose_name
