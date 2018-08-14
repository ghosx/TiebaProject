from django.db import models


class User(models.Model):
    bduss = models.CharField(max_length=192,verbose_name="BDUSS")
    username = models.CharField(max_length=30,verbose_name="贴吧用户名")
    token = models.CharField(max_length=200,unique=True,verbose_name="个人TOKEN")
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="提交时间")
    modified_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")
    is_activite = models.BooleanField(default=True,verbose_name="是否活动")
    i_type = models.BooleanField(default=True,verbose_name="云回模式")  # True为客户端模式


    def __str__(self):
        return self.username

    class Mete:
        get_latest_by = "created_time"
        table_name = 'user'
        ordering = ['created_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Tieba(models.Model):
    name = models.CharField(max_length=40,verbose_name="贴吧名")
    fid = models.CharField(max_length=20,verbose_name="贴吧id")
    tid = models.CharField(max_length=20, verbose_name="帖子id")
    isLou = models.BooleanField(default=False,verbose_name="是否楼中楼")
    floor = models.CharField(max_length=20,null=True,blank=True,verbose_name="楼层数")
    qid = models.CharField(max_length=20,null=True,blank=True,verbose_name="楼层数id")
    time = models.IntegerField(verbose_name="回复间隔",default=5)
    success = models.IntegerField(null=True, default=0, verbose_name="成功次数")
    fail = models.IntegerField(null=True, default=0, verbose_name="失败次数")
    stop = models.BooleanField(default=False,verbose_name="是否暂停")
    stop_times = models.IntegerField(null=True, default=0, verbose_name="暂停次数")
    add_time = models.DateTimeField(auto_now_add=True,verbose_name="插入时间")
    user = models.ManyToManyField(User, verbose_name="所属用户")

    def __str__(self):
        return self.name

    class Mete:
        get_latest_by = "add_time"
        table_name = 'tieba'
        ordering = ['add_time']
        verbose_name = '贴吧'
        verbose_name_plural = verbose_name


class Sign(models.Model):
    name = models.CharField(max_length=100,verbose_name="贴吧名")
    fid = models.CharField(max_length=20,verbose_name="贴吧id")
    level_id = models.IntegerField(null=True, default=0, verbose_name="当前等级")
    cur_score = models.IntegerField(null=True, default=0, verbose_name="当前经验")
    is_sign = models.BooleanField(default=False,verbose_name="是否签到")
    user = models.ManyToManyField(User, verbose_name="所属用户")

    def __str__(self):
        return self.name