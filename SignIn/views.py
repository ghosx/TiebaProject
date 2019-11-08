# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
import uuid
from SignIn.models import User, Sign
from django.shortcuts import reverse
import logging
import requests
import json
import time
import random

from SignIn.utils import utils

# Create your views here.
logging.basicConfig(filename='app.log', format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d')


def index(request):
    if request.method == "GET":
        data = {}
        data['user'] = User.objects.all().count()
        data['sign'] = Sign.objects.filter(is_sign=True).count()
        data['unsign'] = Sign.objects.filter(is_sign=False).count()
        return render(request, 'index.html', {'data': data})
    elif request.method == "POST":
        bduss = request.POST.get('bduss', None)
        if bduss is None:
            return redirect(reverse(info))
        if len(bduss) != 192:
            return render(request, 'index.html', {'msg': 'BDUSS错误～'})
        name = utils.get_name(bduss)
        if not name:
            return render(request, 'index.html', {'msg': 'BDUSS错误～'})
        token = str(uuid.uuid1())
        try:
            user = User.objects.get(username=name)
            user.bduss = bduss
        except Exception:
            user = User(bduss=bduss, username=name, token=token)
        finally:
            user.save()
            request.session['user'] = user.username
            request.session['token'] = user.token
            return redirect(reverse(info))
    else:
        return render(request, 'error.html')




def info(request):
    if request.method == "GET":
        token = request.session.get('token')
        if not token:
            return render(request, 'info.html')
        user = User.objects.get(token=token)
        allbind = user.all_bind
        signed = user.signed
        unsigned = user.unsigned
        return render(request, 'info.html',
                      {'allbind': allbind, 'signed': signed, 'unsigned': unsigned, 'username': user.username})
    else:
        return redirect('/')



def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        val = request.POST.get('unsure')
        if len(val) != 36:
            return render(request, 'login.html', {'msg': 'SECRET 错误'})
        else:
            try:
                u = User.objects.get(token=val)
                request.session['user'] = u.username
                request.session['token'] = u.token
                return redirect(reverse(info))
            except Exception:
                return render(request, 'login.html', {'msg': 'SECRET 错误'})


def logout(request):
    del request.session['user']
    del request.session['token']
    return redirect(reverse(index))


def bduss(request):
    s = requests.session()
    if request.method == 'GET':
        url1 = 'https://passport.baidu.com/v2/api/getqrcode?lp=pc&apiver=v3&tpl=netdisk'
        headers1 = {
            'Connection': 'keep-alive',
            'Host': 'passport.baidu.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        res1 = s.get(url=url1, headers=headers1).json()
        global sign
        sign = res1['sign']
        print(sign)
        imgurl = 'https://' + res1['imgurl']
        return render(request, 'bduss.html', {'img': imgurl})
    elif request.method == 'POST':
        url2 = 'https://passport.baidu.com/channel/unicast?channel_id={}&callback=&tpl=netdisk&apiver=v3'.format(sign)
        headers2 = {
            'Host': 'passport.baidu.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        res2 = s.get(url=url2, headers=headers2).text[1:-2]
        data = json.loads(res2)
        data = json.loads(data['channel_v'])
        v = data['v']
        url3 = 'https://passport.baidu.com/v3/login/main/qrbdusslogin?bduss={}&u=https%253A%252F%252Fpan.baidu.com%252Fdisk%252Fhome&loginVersion=v4&qrcode=1&tpl=netdisk&apiver=v3&traceid=&callback=%27'.format(
            v)
        response = s.get(url3)
        bduss = response.cookies['BDUSS']
        if bduss is None:
            return render(request, 'bduss.html', {'bduss': bduss})
        print(len(bduss))
        print(bduss)
        if len(bduss) != 192:
            return render(request, 'index.html', {'msg': 'BDUSS错误～'})
        name = utils.get_name(bduss)
        print(name)
        if not name:
            return render(request, 'index.html', {'msg': "BDUSS错误"})
        token = str(uuid.uuid1())
        try:
            user = User.objects.get(username=name)
            user.bduss = bduss
        except Exception:
            user = User(bduss=bduss, username=name, token=token)
        finally:
            user.save()
            request.session['user'] = user.username
            request.session['token'] = user.token
            return render(request, 'success.html', {'username': user.username})


def about(request):
    return render(request, 'about.html')

