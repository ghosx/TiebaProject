# -*- coding:utf-8 -*-
import requests
import re
import hashlib
import time
import copy

from constants import *


def get_tbs(bduss):
    headers = HEADERS.update({COOKIE: EMPTY_STR.join([BDUSS, EQUAL, bduss])})
    return requests.get(url=TBS_URL, headers=headers).json()[TBS]

def get_name(bduss):
    # 网页版获取贴吧用户名
    headers = HEADERS.update({COOKIE: EMPTY_STR.join([BDUSS, EQUAL, bduss])})
    try:
        r = requests.get(url=GET_USERNAME_URL, headers=headers).text
        name = re.search(USERNAME_REGEX, r).group(1)
        return name
    except Exception:
        return None

def get_favorite(bduss):
    # 客户端关注的贴吧
    i = 1
    data = copy.copy(SIMPLE_PARA)
    data = data.update({BDUSS: bduss, PAGE_NO: ONE, TIMESTAMP: str(int(time.time())), })
    data = encodeData(data)
    res = requests.post(url=LIKIE_URL, data=data, timeout=2).json()
    return_data = res
    if FORM_LIST not in return_data:
        return_data[FORM_LIST] = []
    if not res[FORM_LIST]:
        return {GCONFORM: [], NON_GCONFORM: []}
    if NON_GCONFORM not in return_data[FORM_LIST]:
        return_data[FORM_LIST][NON_GCONFORM] = []
    if GCONFORM not in return_data[FORM_LIST]:
        return_data[FORM_LIST][GCONFORM] = []
    while HAS_MORE in res and res[HAS_MORE] == ONE:
        i = i + 1
        data[PAGE_NO] = str(i)
        data = encodeData(data)
        res = requests.post(url=LIKIE_URL, data=data, timeout=2).json()
        if NON_GCONFORM in res[FORM_LIST]:
            return_data[FORM_LIST][NON_GCONFORM].append(res[FORM_LIST][NON_GCONFORM])
        if GCONFORM in res[FORM_LIST]:
            return_data[FORM_LIST][GCONFORM].append(res[FORM_LIST][GCONFORM])
    return return_data


def get_fid(bdname):
    # 获取贴吧对用的fourm id
    fid = requests.get(url=FID_URL.format(bdname), timeout=2).json()[DATA][FID]
    return fid


def encodeData(data):
    s = EMPTY_STR
    keys = data.keys()
    for i in sorted(keys):
        s = EMPTY_STR.join([s, i, EQUAL, str(data[i])])
    sign = hashlib.md5((s + SIGN_KEY).encode(UTF8)).hexdigest().upper()
    data.update({SIGN: str(sign)})
    return data


def client_Sign(bduss, kw, fid, tbs):
    # 客户端签到

    data = {
        "BDUSS": bduss,
        '_client_type': '2',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        "fid": fid,
        'kw': kw,
        'model': 'MI+5',
        "net_type": "1",
        'tbs': tbs,
        'timestamp': str(int(time.time())),
    }
    data = encodeData(data)
    res = requests.post(url=SIGN_URL, data=data, timeout=1).json()
    return res


def check(bduss):
    # 检查bduss是否失效
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url=url, headers=headers).json()['is_login']


if __name__ == '__main__':
    bduss = 'Y0U0dvVXhyTng3eFhhTzZ1bTVQUEhPc29DajZsaWpZa0hwR35NckQ1SWpPelJkSVFBQUFBJCQAAAAAAAAAAAEAAAC~0QE4x-u90M7SssrJq18AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACOuDF0jrgxdbn'
    name = get_name(bduss)
    print(name)
