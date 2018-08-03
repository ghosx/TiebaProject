from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from . import utils
import uuid
from .models import TiebaYunHui,TiebaUser
import json


# Create your views here.
stoken = 'e7f5d88e4f9128fe12a5b0d76f9ec21c59a006e1b720bf4dd83c14dd645ad5c1'


def index(request):
    if request.method == "GET":
        return render(request,'index.html')
    elif request.method == "POST":
        bduss = request.POST.get('bduss','default')
        email = request.POST.get('email','default')
        if len(bduss) != 192:
            return HttpResponse('BDUSS长度错误')
        else:
            name,reply,at = utils.getNameReplyAtByBduss(bduss)
            if name:
                token = str(uuid.uuid1())
                try:
                    user = TiebaUser.objects.get(username=name)
                    user.idDel = False;
                    user.bduss=bduss
                    user.email=email
                except Exception:
                    user = TiebaUser(bduss=bduss, username=name, email=email, token=token)
                finally:
                    user.save()
                    request.session['user'] = user.username
                    return redirect('addTz')
            else:
                return HttpResponse("BDUSS以失效")


def delUser(request,uuid):
    if request.method != "GET":
        return HttpResponse("请求方法错误")
    elif request.method == "GET":
        token = uuid
        try:
            user = TiebaUser.objects.get(token=token)
        except Exception :
            return HttpResponse("TOKEN有误，未查到相关用户")
        if user.idDel:
            return HttpResponse("用户不存在")
        user.idDel = True
        user.save()
        return HttpResponse("删除成功")


def addTz(request):
    user = request.session.get('user')
    if user:
        return render(request,'add.html')
    else:
        return redirect('index')

def addtieze(request):
    if request.method == 'GET':
        return render(request,'add.html')
    elif request.method == 'POST':
        username = request.session.get('user')
        user = TiebaUser.objects.get(username=username)
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
        t = TiebaYunHui(name=tbna,fid=fid,tid=tid,isLou=louBin,floor=floor,qid=Qid)
        t.save()
        t.user.add(user)
        t.save()
        return HttpResponse('aaa')



