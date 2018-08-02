from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from . import utils
import uuid
from .models import Tieba,User


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
                request.session['token'] = token
                request.session['name'] = name
                request.session['email'] = email
                try:
                    user = User.objects.get(username=name)
                    user.idDel = False;
                    user.bduss=bduss
                    user.email=email
                except Exception:
                    user = User(bduss=bduss, username=name, email=email, token=token)
                finally:
                    user.save()
                    return redirect('addTz')
            else:
                return HttpResponse("BDUSS以失效")


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


def addTz(request):
    name = request.session.get('name')
    if name:
        return render(request,'add.html')
    else:
        return redirect('index')

def addtieze(request):
    if request.method == 'GET':
        return render(request,'add.html')

