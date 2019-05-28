from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import utils
import uuid
from .models import Tieba, User, Sign, Data, Robot
from django.shortcuts import reverse
import logging
import requests
import json
import time
import random

# Create your views here.
logging.basicConfig(filename='app.log', format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d')


def test(request):
    return HttpResponse('test')


def index(request):
    if request.method == "GET":
        data = {}
        data['user'] = User.objects.all().count()
        data['yunhui'] = Data.objects.get(id=1).success
        data['sign'] = Sign.objects.filter(is_sign=True).count()
        data['unsign'] = Sign.objects.filter(is_sign=False).count()
        return render(request, 'index.html', {'data': data})


def info(request):
    if request.method == "GET":
        token = request.session.get('token', None)
        if token:
            u = User.objects.get(token=token)
            t = u.tieba_set.all()
            allbind = u.绑定贴吧
            signed = u.已签到
            unsigned = u.未签到
            return render(request, 'info.html', {'data': t, 'allbind': allbind, 'signed': signed, 'unsigned': unsigned,
                                                 'username': u.username})
        else:
            return render(request, 'info.html')
    elif request.method == "POST":
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
            return render(request, 'add.html', {'msg': '测试阶段限制每人5条帖子', 'type': 'error'})
        lou = request.POST.get('lou')
        tid = request.POST.get('tid')
        _time = request.POST.get('time')
        floor = request.POST.get('floor')
        tbna = utils.get_kw(tid)
        fid = utils.get_fid(tbna)
        if lou == 'yes':
            louBin = True
            Qid = utils.get_qid(tid, floor)
        elif lou == 'no':
            louBin = False
            Qid = None
        t = Tieba(name=tbna, fid=fid, tid=tid, isLou=louBin, floor=floor, qid=Qid, time=_time, user_id=user.pk)
        t.save()
        msg = '帖子' + tid + '添加成功'
        return render(request, 'add.html', {'msg': msg})


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
        if bduss is not None:
            if len(bduss) != 192:
                return render(request, 'index.html', {'msg': 'BDUSS错误～'})
            name = utils.get_name(bduss)
            if name:
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
            else:
                return render(request, 'index.html', {'msg': "BDUSS错误"})
        else:
            return render(request, 'bduss.html', {'bduss': bduss})


def about(request):
    return render(request, 'about.html')


def robot(request):
    return render(request, 'robot.html')


def random1(request):
    # t模拟随机延迟
    t = random.randint(1, 2) / 10
    time.sleep(t)
    return HttpResponse(t)


def newLogin(request):
    a = {
        "data": {
            "PrjName": "西安理工大学蓝牙系统",
            "TelPhone": 13888888888,
            "alipay_user_id": "null",
            "loginCode": "8888",
            "AccMoney": 99999,
            "GivenAccMoney": 99999,
            "AccStatusID": 0,
            "GroupID": 2,
            "tags": "alLyrelease,84",
            "agreement_no": "null",
            "alias": "13888888888",
            "AccID": 11049,
            "PrjID": 84
        },
        "error_code": "0",
        "message": "登录成功"
    }
    response = HttpResponse(json.dumps(a))
    return response


def accountInfo(request):
    a = {
        "data": {
            "PrjName": "",
            "TelPhone": 13888888888,
            "AccMoney": 999999,
            "GivenAccMoney": 999999,
            "AccStatusID": 0,
            "AccID": 11049,
            "PrjID": 84,
            "GroupID": 2
        },
        "error_code": "0",
        "message": "获取账户信息成功"
    }
    return HttpResponse(json.dumps(a))


def queryPushMsg(request):
    a = {
        "data": [],
        "error_code": "0"
    }
    return HttpResponse(json.dumps(a))


def versionCheck(request):
    a = {
        "error_code": "0",
        "message": "当前已是最新版本",
        "url": ""
    }
    return HttpResponse(json.dumps(a))


def priinfo(request):
    a = {
        "data": {
            "ServerTel": "4008828051",
            "UserID": 34,
            "PrjName": "",
            "PrjYKMoney": 5.0000,
            "IsUse": 1,
            "WXPartnerKey": "",
            "PrjDescript": "",
            "WXAPPID": "",
            "WXPartner": "",
            "WXSevret": "",
            "PrjID": 84
        },
        "error_code": "0"
    }
    return HttpResponse(json.dumps(a))


def deviceInfo(request):
    mac = request.GET.get("deviceMac_List")
    a = {
        "data": [
            {
                "DevName": "Just Do IT",
                "QUName": "",
                "FJName": "",
                "PrjName": "",
                "IsUse": 1,
                "LCName": "",
                "DevDescript": "",
                "Dsbtypeid": 5,
                "LDID": 230,
                "LDName": "",
                "DsbName": "",
                "devMac": mac,
                "LCID": 237,
                "DevTypeName": "",
                "DevTypeID": 51,
                "QUID": 1,
                "DevStatusID": 0,
                "DevID": 31,
                "PrjID": 84,
                "FJID": 257
            }
        ],
        "error_code": "0"
    }
    return HttpResponse(json.dumps(a))


def downRate(request):
    a = {
        "LeadMoneyReal": 0,
        "data": {
            "Rate1": 40,
            "MinMoney": 0,
            "Rate3": 38,
            "Rate2": 38,
            "signature": "b6e9043f9c79436ef3d2bb15d38fad53",
            "AutoDisConTime": 6,
            "UseCount": 146,
            "MinChargeUnit": 10,
            "AccStatusID": 0,
            "ParaTypeID": 1,
            "PerMoney": 5000,
            "ConsumeDT": "20181115234427",
            "ChargeMethod": 17,
            "DevStatusID": 0,
            "MinTime": 0
        },
        "LeadMoneyGiven": 0,
        "error_code": "0",
        "message": "成功"
    }
    return HttpResponse(json.dumps(a))


def savexf(request):
    a = {
        "UpLeadMoney": 99999,
        "UpMoney": 0,
        "FishTime": "2018-01-01 00:00:00",
        "error_code": "0",
        "PerMoney": 2000
    }
    return HttpResponse(json.dumps(a))


def querySpread(request):
    a = {
        "data": [
            {
                "spreadPIC": "",
                "spreadTitle": "性感学长，在线打水",
                "spreadURL": "",
                "createrDT": "",
                "spreadContent": "↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑"
            },
            {
                "spreadPIC": "",
                "spreadTitle": "==重要==",
                "spreadURL": "",
                "createrDT": "",
                "spreadContent": "请不要分享给他人，否则后果自负"
            }
        ],
        "error_code": "0",
        "message": "获取成功"
    }
    return HttpResponse(json.dumps(a))


def infoSel(request):
    a = {
        "data": {
            "AccMoney": 999900,
            "PrjID": 84
        },
        "error_code": "0"
    }
    return HttpResponse(json.dumps(a))
