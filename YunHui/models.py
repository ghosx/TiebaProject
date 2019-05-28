from django.db import models


class User(models.Model):
    bduss = models.CharField(max_length=192, verbose_name="BDUSS")
    username = models.CharField(max_length=30, unique=True, editable=False, verbose_name="贴吧用户名")
    token = models.CharField(max_length=200, unique=True, editable=False, verbose_name="个人TOKEN")
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="提交时间")
    modified_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    flag = models.IntegerField(null=True, default=0, verbose_name="新用户")  # 默认0 已update1 已sign2
    i_type = models.BooleanField(default=True, verbose_name="云回模式")  # True为客户端模式

    def __str__(self):
        return self.username

    @property
    def 绑定贴吧(self):
        return self.sign_set.all().count()

    @property
    def 已签到(self):
        return self.sign_set.all().filter(is_sign=1).count()

    @property
    def 未签到(self):
        return self.sign_set.all().filter(is_sign=0).count()

    def 云回贴吧(self):
        return self.tieba_set.all().count()

    class Mete:
        get_latest_by = "created_time"
        table_name = 'user'
        ordering = ['created_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Tieba(models.Model):
    name = models.CharField(max_length=40, verbose_name="贴吧名")
    fid = models.CharField(max_length=20, verbose_name="贴吧id")
    tid = models.CharField(max_length=20, verbose_name="帖子id")
    isLou = models.BooleanField(default=False, verbose_name="是否楼中楼")
    floor = models.CharField(max_length=20, null=True, blank=True, verbose_name="楼层数")
    qid = models.CharField(max_length=20, null=True, blank=True, verbose_name="楼层数id")
    time = models.IntegerField(verbose_name="回复间隔", default=5)
    success = models.IntegerField(null=True, default=0, verbose_name="成功次数")
    fail = models.IntegerField(null=True, default=0, verbose_name="失败次数")
    stop = models.BooleanField(default=False, verbose_name="是否暂停")
    stop_times = models.IntegerField(null=True, default=0, verbose_name="暂停次数")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="插入时间")
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name="所属用户",)

    def __str__(self):
        return self.name

    class Mete:
        get_latest_by = "add_time"
        table_name = 'tieba'
        ordering = ['add_time']
        verbose_name = '贴吧'
        verbose_name_plural = verbose_name


class Sign(models.Model):
    name = models.CharField(max_length=100, verbose_name="贴吧名")
    fid = models.CharField(max_length=20, verbose_name="贴吧id")
    level_id = models.IntegerField(null=True, default=0, verbose_name="当前等级")
    cur_score = models.IntegerField(null=True, default=0, verbose_name="当前经验")
    is_sign = models.BooleanField(default=False, verbose_name="是否签到")
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="所属用户")

    def __str__(self):
        return self.name

    class Mete:
        table_name = 'sign'
        verbose_name = '签到'
        verbose_name_plural = verbose_name


class Data(models.Model):
    success = models.IntegerField(null=True, default=0, blank=True, verbose_name="云回成功总数")

    def __str__(self):
        return self.success

    class Mete:
        table_name = 'data'
        verbose_name = '数据汇总'
        verbose_name_plural = verbose_name

class Robot(models.Model):
    thread_id = models.CharField(max_length=20,null=True, blank=True,verbose_name="帖子id")
    post_id = models.CharField(max_length=20, verbose_name="楼层数id")
    title = models.CharField(max_length=200, verbose_name="标题")
    username = models.CharField(max_length=200,verbose_name="用户名")
    is_fans = models.BooleanField(default=False, verbose_name="是粉丝")
    fname = models.CharField(max_length=20,verbose_name='贴吧名')
    content = models.CharField(max_length=200,verbose_name='内容')
    time = models.CharField(max_length=20,verbose_name='时间')

    def __str__(self):
        return self.username+'在'+self.fname+'@了我'

    class Mete:
        table_name = 'robot'
        verbose_name = '机器人'
        verbose_name_plural = verbose_name

