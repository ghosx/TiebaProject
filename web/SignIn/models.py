# -*- coding:utf-8 -*-
import time
import uuid
import logging

from django.db import models
from django.db.models import F
from django.core.mail import send_mail, send_mass_mail

from SignIn.utils import utils
from constants import NOT_VALID_USER, ALREADY_UPDATE_USER, NEW_USER, API_STATUS, MAX_RETRY_TIMES, DEFAULT_EMAIL, \
    DEFAULT_PASSWORD

from django.contrib.auth.models import User as U, Permission
from django.utils.html import format_html
from django.conf import settings

logs = logging.getLogger("task")


class UserManager(models.Manager):

    def new(self, bduss):
        try:
            name = utils.get_name(bduss)
        except Exception as e:
            logs.error(e)
        token = str(uuid.uuid1())
        obj, created = User.objects.update_or_create(username=name,
                                                     defaults={"bduss": bduss, "token": token, "flag": NEW_USER})
        if not U.objects.filter(username=name).exists():
            u = U.objects.create_user(
                username=name, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD)
            u.is_staff = True
            # sign_group
            u.groups.add(1)
            u.save()
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
        logs.info("重置所有用户的贴吧关注状态")
        User.objects.filter(flag=ALREADY_UPDATE_USER).update(flag=NEW_USER)

    @staticmethod
    def set_status_liking():
        """
        修改状态位，不需要更新关注的贴吧
        :return:
        """
        User.objects.filter(flag=NEW_USER).update(flag=ALREADY_UPDATE_USER)

    @staticmethod
    def check_all_user_valid():
        users = User.objects.filter(flag=ALREADY_UPDATE_USER)
        for user in users:
            if not user.valid_user():
                msg = "|".join([user.username, '失效'])
                logs.warning(msg)
                user.flag = NOT_VALID_USER
                user.save()
                # 邮件通知
                user.daliy_notice()


class User(models.Model):
    bduss = models.CharField(max_length=192, verbose_name="BDUSS")
    username = models.CharField(
        max_length=30, unique=True, editable=False, verbose_name="贴吧用户名")
    token = models.CharField(max_length=100, unique=True,
                             editable=False, verbose_name="个人TOKEN")
    created_time = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="提交时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    flag = models.IntegerField(
        null=True, default=0, verbose_name="新用户")  # 默认0 已update1 bduss失效2
    email = models.EmailField(
        max_length=100, blank=True, null=True, verbose_name="邮箱")
    email_notice = models.BooleanField(default=False, verbose_name="是否通知")
    objects = UserManager()

    def daliy_notice(self):
        # 邮件通知
        logs.info("邮件通知")
        if self.email_notice and self.email:
            emial_from = settings.EMAIL_FROM
            today = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            # bduss 失效通知
            title = "BDUSS失效通知"
            site_url = settings.SITE_URL
            content = f"账号：{self.username}\r\nBDUSS失效！\r\n请尽快前往【{site_url}】扫码更新"
            res = send_mail("--".join([title, today]), content,
                            emial_from, (self.email,), fail_silently=False)
            logs.info("|".join(["邮件通知", self.username, "成功" if res else "失败"]))
        else:
            logs.error("|".join([self.username, "未配置邮件通知"]))

    @property
    def 是否有效用户(self):
        # 定义显示的颜色，male显示蓝色，female显示红色
        is_valid_user = self.flag != NOT_VALID_USER
        if is_valid_user:
            html = '<span style="color: green;">{}</span>'
        else:
            html = '<span style="color: red;">{}</span>'
        return format_html(
            html,
            '有效' if is_valid_user else '无效',
        )

    @property
    def 共关注(self):
        return self.sign_set.count()

    @property
    def 已签到(self):
        return self.sign_set.filter(is_sign=1).exclude(status="").count()

    @property
    def 未签到(self):
        return self.共关注 - self.已签到

    def __str__(self):
        return self.username

    def like(self):
        res = utils.get_favorite(self.bduss)
        return res

    def like_callback(self, res):
        res = res.result()
        signs = []
        fids = []
        for i in res:
            fid, name = i["id"], i["name"]
            try:
                Sign.objects.get(fid=fid, name=name, user=self)
            except Sign.DoesNotExist:
                # 去重处理
                if fid not in fids:
                    msg = "|".join([self.username, "获取到新关注的贴吧:", name])
                    logs.info(msg)
                    fids.append(fid)
                    signs.append(Sign(fid=fid, name=name, user=self))
        try:
            Sign.objects.bulk_create(signs)
        except Exception as e:
            logs.error(e)

    def valid_user(self):
        try:
            res = utils.check_bduss(self.bduss)
        except Exception as e:
            logs.error(e)
        return res

    class Meta:
        get_latest_by = "created_time"
        db_table = 'user'
        ordering = ['-update_time']
        verbose_name = r"用户"
        verbose_name_plural = verbose_name


class SignManager(models.Manager):

    @staticmethod
    def need_sign():
        # 查找出未签到且用户为有效用户的贴吧
        obj = Sign.objects.filter(is_sign=False).exclude(
            user__flag=NOT_VALID_USER).select_related("user")
        return obj

    @staticmethod
    def reset_sign_status_again():
        logs.info("再次重置所有贴吧的签到状态")
        Sign.objects.filter(is_sign=True, status="").exclude(user__flag=NOT_VALID_USER).update(
            is_sign=False, retry_time=0)

    @staticmethod
    def reset_sign_status():
        logs.info("重置所有贴吧的签到状态")
        Sign.objects.filter(is_sign=True).exclude(user__flag=NOT_VALID_USER).update(is_sign=False, status="",
                                                                                    retry_time=0)

    def set_status_signing(self):
        Sign.objects.filter(is_sign=False).update(is_sign=True)


class Sign(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    fid = models.CharField(max_length=20, verbose_name="贴吧id")
    is_sign = models.BooleanField(default=False, verbose_name="是否签到")
    retry_time = models.SmallIntegerField(default=0, verbose_name="重试次数")
    status = models.CharField(max_length=100, verbose_name="签到状态", default="")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="所属用户")
    objects = SignManager()

    def __str__(self):
        return self.name

    def sign(self):
        u = self.user
        try:
            res = utils.client_sign(bduss=u.bduss, sign=self)
        except Exception as e:
            logs.error(e)
        finally:
            return {"res": res, 'sign': self}

    def sign_callback(self, obj):
        result = obj.result()
        res = result["res"]
        sign = result["sign"]
        # 判断res是否为None,即签到过程中有没有发生异常
        if not res:
            self.objects.update(
                is_sign=False, status="网络发生异常", retry_time=F('retry_time') + 1)
        else:
            # res 为有效值，开始判断签到情况
            error_code = str(res.get('error_code', 0))

            if error_code in API_STATUS:
                self.is_sign = True
                self.status = API_STATUS[error_code]
                # 只有签到成功的时候进行 日志记录
                msg = "|".join(["签到成功", sign.user.username, sign.name])
                logs.info(msg)
                SignLog.objects.log(sign, res)
            else:
                # 如果尝试签到3次还未成功，则不再尝试
                if self.retry_time >= MAX_RETRY_TIMES:
                    self.is_sign = True
                    self.status = "超过最大签到重试次数"
                    # 只有签到成功的时候进行 日志记录
                    SignLog.objects.log(sign, res)
                else:
                    self.is_sign = False
                    self.retry_time += 1
                    self.status = res.get('error_msg', "未知错误")
                msg = '|'.join(
                    ['签到出错', sign.user.username, sign.name, self.status])
                logs.error(msg)
            self.save()

    class Meta:
        db_table = 'sign'
        verbose_name = '签到'
        verbose_name_plural = verbose_name
        unique_together = (('name', 'fid', 'user'),)


class SignLogManager(models.Manager):

    @staticmethod
    def log(sign, ret_log):
        # 写日志
        SignLog.objects.update_or_create(
            name=sign.name, user=sign.user, defaults={"ret_log": ret_log})
        # 更新签到总数
        SignTotal.objects.update(number=F('number') + 1)


class SignLog(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="所属用户")
    ret_log = models.TextField(verbose_name="签到日志")
    objects = SignLogManager()

    class Meta:
        db_table = 'sign_log'
        ordering = ['-update_time']
        verbose_name = '签到日志'
        verbose_name_plural = verbose_name


class SignTotal(models.Model):
    number = models.IntegerField()

    class Meta:
        db_table = 'sign_total'
        verbose_name = '签到总数'
        verbose_name_plural = verbose_name
