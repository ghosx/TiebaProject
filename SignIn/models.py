# -*- coding:utf-8 -*-
import time
import uuid

from django.db import models
from django.db.models import Q

from SignIn.utils import utils
from constants import MAX_RETRY_TIMES, NOT_VALID_USER, ALREADY_UPDATE_USER, NEW_USER


class UserManager(models.Manager):

    def new(self, bduss):
        name = utils.get_name(bduss)
        token = str(uuid.uuid1())
        obj, created = User.objects.update_or_create(username=name,
                                                     defaults={"bduss": bduss, "token": token, "flag": NEW_USER})
        return created

    @staticmethod
    def need_update_like():
        """
        返回需要更新关注贴吧的用户
        :return:
        """
        return User.objects.filter(flag=NEW_USER)

    @staticmethod
    def re_update_like():
        """
        修改状态位，重新更新关注的贴吧
        :return:
        """
        print(time.time(), "重置所有用户的贴吧关注状态")
        User.objects.filter(flag=ALREADY_UPDATE_USER).update(flag=NEW_USER).save()

    @staticmethod
    def set_status_liking():
        """
        修改状态位，不需要更新关注的贴吧
        :return:
        """
        User.objects.filter(flag=NEW_USER).update(flag=ALREADY_UPDATE_USER)

    @staticmethod
    def check_all_user_valid():
        users = User.objects.all()
        for user in users:
            if not user.valid_user():
                print(time.time(), user.username, '失效')
                user.flag = NOT_VALID_USER
                user.save()


class User(models.Model):
    bduss = models.CharField(max_length=192, verbose_name="BDUSS")
    username = models.CharField(max_length=30, unique=True, editable=False, verbose_name="贴吧用户名")
    token = models.CharField(max_length=200, unique=True, editable=False, verbose_name="个人TOKEN")
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="提交时间")
    flag = models.IntegerField(null=True, default=0, verbose_name="新用户")  # 默认0 已update1 bduss失效2
    objects = UserManager()

    @property
    def 是否有效用户(self):
        return self.flag != 2

    @property
    def 共关注(self):
        return self.sign_set.count()

    @property
    def 已签到(self):
        return self.sign_set.filter(is_sign=1).count()

    @property
    def 未签到(self):
        return self.sign_set.filter(is_sign=0).count()

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

    def valid_user(self):
        return utils.check_bduss(self.bduss)

    class Meta:
        get_latest_by = "created_time"
        db_table = 'user'
        ordering = ['created_time']
        verbose_name = r"用户"
        verbose_name_plural = verbose_name


class SignManager(models.Manager):

    @staticmethod
    def need_sign():
        # 查找出未签到且用户为有效用户的贴吧
        obj = Sign.objects.filter(is_sign=False).filter(~Q(user__flag=NOT_VALID_USER))
        return obj

    @staticmethod
    def reset_sign_status():
        print(time.time(), "重置所有贴吧的签到状态")
        Sign.objects.filter(is_sign=True).update(is_sign=False, retry_times=0, status="").save()

    def set_status_signing(self):
        Sign.objects.filter(is_sign=False).update(is_sign=True).save()


class Sign(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    fid = models.CharField(max_length=20, verbose_name="贴吧id")
    is_sign = models.BooleanField(default=False, verbose_name="是否签到")
    status = models.CharField(max_length=100, verbose_name="签到状态", default="")
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
        # 如果尝试签到3次还未成功，则不再尝试
        if self.retry_times >= MAX_RETRY_TIMES:
            self.status = "最大尝试次数"
        elif str(res['error_code']) == '0':
            self.status = "签到成功"
        else:
            # 签到状态判断
            self.is_sign = False
            self.retry_times += 1
            self.status = res['error_msg']
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
