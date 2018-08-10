from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import utils
import uuid
from .models import Tieba, User
from django.shortcuts import reverse
import logging

# Create your views here.
logging.basicConfig(filename='app.log', format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d')


def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    elif request.method == "POST":
        bduss = request.POST.get('bduss', 'default')
        if len(bduss) != 192:
            return render(request, 'index.html', {'msg': 'BDUSS长度错误～'})
        else:
            name, reply, at = utils.getNameReplyAtByBduss(bduss)
            if name:
                token = str(uuid.uuid1())
                try:
                    user = User.objects.get(username=name)
                    user.idDel = False
                    user.bduss = bduss
                except Exception:
                    user = User(bduss=bduss, username=name, token=token)
                finally:
                    user.save()
                    request.session['user'] = user.username
                    request.session['token'] = user.token
                    return redirect(reverse(info))
            else:
                return redirect(reverse(info))


def info(request):
    if request.method == "GET":
        token = request.session.get('token', None)
        if token:
            u = User.objects.get(token=token)
            t = u.tieba_set.all()
            return render(request, 'info.html', {'data': t})
        else:
            return render(request, 'info.html')
    elif request.method == "POST":
        return redirect('/')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        val = request.POST.get('unsure')
        print(val)
        if (len(val) != 192) and (len(val) != 36):
            return render(request, 'login.html', {'msg': 'BDUSS或TOKEN长度错误'})
        elif len(val) == 192:
            try:
                u = User.objects.get(bduss=val)
                request.session['user'] = u.username
                request.session['token'] = u.token
                return redirect(reverse(info))
            except Exception:
                return render(request, 'login.html', {'msg': 'BDUSS错误'})
        elif len(val) == 36:
            try:
                u = User.objects.get(token=val)
                request.session['user'] = u.username
                request.session['token'] = u.token
                return redirect(reverse(info))
            except Exception:
                return render(request, 'login.html', {'msg': 'TOKEN错误'})


def logout(request):
    del request.session['user']
    del request.session['token']
    return redirect(reverse(index))


def delete(request, id):
    if request.method == "POST":
        return HttpResponse("请求方法错误")
    elif request.method == "GET":
        user = request.session.get('user', None)
        if user:
            try:
                u = User.objects.get(username=user)
                t = Tieba.objects.get(id=id, user=u)
                t.delete()
                return HttpResponse('success')
            except Exception:
                return render(request, 'info.html', {'msg': '越权访问'})
        else:
            return render(request, 'info.html', {'msg': '未登录'})


def switch(request, id):
    if request.method == "POST":
        return HttpResponse("请求方法错误")
    elif request.method == "GET":
        user = request.session.get('user', None)
        if user:
            try:
                u = User.objects.get(username=user)
                t = Tieba.objects.get(id=id, user=u)
                if t.stop:
                    t.stop = False
                else:
                    t.stop = True
                t.save()
                return HttpResponse('success')
            except Exception:
                return render(request, 'info.html', {'msg': '越权访问'})
        else:
            return render(request, 'info.html', {'msg': '未登录'})


def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    elif request.method == 'POST':
        username = request.session.get('user')
        user = User.objects.get(username=username)
        # 测试阶段限制每人5条帖子
        tielist = user.tieba_set.all().count()
        if tielist >= 5:
            return render(request, 'add.html', {'msg': '测试阶段限制每人5条帖子','type':'error'})
        lou = request.POST.get('lou')
        tid = request.POST.get('tid')
        _time = request.POST.get('time')
        floor = request.POST.get('floor')
        tbna = utils.getFname(tid)
        fid = utils.getFid(tbna)
        if lou == 'yes':
            louBin = True
            Qid = utils.getQid(tid, floor)
        elif lou == 'no':
            louBin = False
            Qid = None
        t = Tieba(name=tbna, fid=fid, tid=tid, isLou=louBin, floor=floor, qid=Qid, time=_time)
        t.save()
        t.user.add(user)
        t.save()
        msg = '帖子' + tid + '添加成功'
        return render(request, 'add.html', {'msg': msg})

def do(request):
    return render(request, 'bduss.html')

def about(request):
    return render(request, 'about.html')

def status(request):
    tie = user.tieba_set.all().count()
    user = User.objects.all().count()
    success = 



