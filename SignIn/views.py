# -*- coding:utf-8 -*-
import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.cache import cache

from SignIn.models import User, Sign, SignLog
import logging
import requests
import json

from constants import QRCODE_URL, QR_CODE_HEADER, SIGN, PASSPORT_URL, LOGIN_URL, BDUSS, CHANNEL_V

logging.basicConfig(filename='app.log', format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d')


def index(request):
    return render(request, 'index.html')


def get_img(request):
    res = requests.get(url=QRCODE_URL, headers=QR_CODE_HEADER).json()
    return JsonResponse(res)


def new(request):
    sign = request.GET.get(SIGN)
    url = PASSPORT_URL.format(sign)
    try:
        res = requests.get(url=url, headers=QR_CODE_HEADER, timeout=2)
    except requests.exceptions.Timeout:
        fuck = HttpResponse("你没扫码你点尼玛的扫码成功呢？")
        fuck.status_code = 404
        return fuck
    res = res.text[1:-2]
    data = json.loads(res)
    data = json.loads(data[CHANNEL_V])
    v = data['v']
    url3 = LOGIN_URL.format(
        v)
    response = requests.get(url3, timeout=2)
    bduss = response.cookies[BDUSS]
    if not bduss:
        fuck = HttpResponse("你没扫码你点尼玛的扫码成功呢？")
        fuck.status_code = 404
        return fuck
    User.objects.new(bduss)
    return HttpResponse('ok')


def status(request):
    if cache.has_key('user_count') and cache.has_key('today_sign') and cache.has_key('total_sign'):
        user_count = cache.get('user_count')
        today_sign = cache.get('today_sign')
        total_sign = cache.get('total_sign')
    else:
        user_count = User.objects.count()
        today_sign = Sign.objects.filter(is_sign=1).filter(~Q(status="")).count()
        total_sign = SignLog.objects.count()

        cache.set('user_count', user_count, 60 * 5)
        cache.set('today_sign', today_sign, 60 * 5)
        cache.set('total_sign', total_sign, 60 * 5)
    return JsonResponse({"user_count": user_count, "today_sign": today_sign, "total_sign": total_sign})
