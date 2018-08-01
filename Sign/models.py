from django.db import models

class Tieba(models.Model):
    name = models.CharField(max_length=40,verbose_name="name")
    tid = models.IntegerField()
    isSign = models.BooleanField(default=False)
    isLike = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(models.Model):
    bduss = models.CharField(max_length=192)
    username = models.CharField(max_length=30,verbose_name="用户名")
    openid = models.CharField(max_length=200,null=True,blank=True,unique=True)
    tb = models.ManyToManyField(Tieba)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    idDel = models.BooleanField(default=False)

    def __str__(self):
        return self.username



