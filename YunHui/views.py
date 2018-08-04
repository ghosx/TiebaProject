from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from . import utils
import uuid
from .models import Tieba,User
import time


# Create your views here.
stoken = 'e7f5d88e4f9128fe12a5b0d76f9ec21c59a006e1b720bf4dd83c14dd645ad5c1'


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    elif request.method == "POST":
        bduss = request.POST.get('bduss','default')
        if len(bduss) != 192:
            return HttpResponse('BDUSS长度错误')
        else:
            name,reply,at = utils.getNameReplyAtByBduss(bduss)
            if name:
                token = str(uuid.uuid1())
                try:
                    user = User.objects.get(username=name)
                    request.session['type'] = '更新'
                    user.idDel = False
                    user.bduss=bduss
                except Exception:
                    user = User(bduss=bduss, username=name, token=token)
                    request.session['type'] = '添加'
                finally:
                    user.save()
                    request.session['user'] = user.username
                    request.session['token'] = user.token
                    return render(request, 'success.html')
            else:
                return render(request, 'success.html')


def delUser(request,uuid):
    if request.method != "GET":
        return HttpResponse("请求方法错误")
    elif request.method == "GET":
        token = uuid
        try:
            user = User.objects.get(token=token)
        except Exception :
            return HttpResponse("TOKEN有误，未查到相关用户")
        if user.idDel:
            return HttpResponse("用户不存在")
        user.idDel = True
        user.save()
        return HttpResponse("删除成功")

def add(request):
    if request.method == 'GET':
        return render(request,'add.html')
    elif request.method == 'POST':
        username = request.session.get('user')
        user = User.objects.get(username=username)
        tbna = request.POST.get('tbname')
        lou = request.POST.get('lou')
        tid = request.POST.get('tid')
        _time = request.POST.get('time')
        floor = request.POST.get('floor')
        fid = utils.getFid(tbna)
        if lou == 'yes':
            louBin = True
            Qid = utils.getQid(tid,floor)
        elif lou == 'no':
            louBin = False
            Qid = None
        t = Tieba(name=tbna, fid=fid, tid=tid, isLou=louBin, floor=floor, qid=Qid,time=_time)
        t.save()
        t.user.add(user)
        t.save()
        return HttpResponse("<script>alert('添加成功');history.go(-1);</script>")

def test(request):
    u = User.objects.all()
    content = "正式测试"
    for i in u:
        for j in i.tieba_set.all():
            if time.localtime().tm_min % j.time == 0:
                if j.isLou:
                    utils.LouZhongLou(i.bduss,content,j.name,j.fid,j.tid,j.qid,j.floor)
                else:
                    utils.HuiTie(i.bduss,content,j.tid,j.fid,j.name)
    return HttpResponse('poi~')

