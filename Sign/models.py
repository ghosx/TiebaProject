from django.db import models


class User(models.Model):
    bduss = models.CharField(max_length=192)
    username = models.CharField(max_length=30,verbose_name="用户名")
    openid = models.CharField(max_length=200,null=True,blank=True,unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    idDel = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Tieba(models.Model):
    name = models.CharField(max_length=40,verbose_name="name")
    fid = models.CharField(max_length=20)
    tbjingyan = models.IntegerField()
    tbdengji = models.IntegerField()
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name





