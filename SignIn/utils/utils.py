# -*- coding:utf-8 -*-
import requests
import re
import hashlib
import time
import copy

from constants import *


def get_tbs(bduss):
    headers = copy.copy(HEADERS)
    headers.update({COOKIE: EMPTY_STR.join([BDUSS, EQUAL, bduss])})
    tbs = requests.get(url=TBS_URL, headers=headers, timeout=2).json()[TBS]
    return tbs


def get_name(bduss):
    # 网页版获取贴吧用户名
    headers = copy.copy(HEADERS)
    headers.update({COOKIE: EMPTY_STR.join([BDUSS, EQUAL, bduss])})
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
    data.update({BDUSS: bduss, PAGE_NO: ONE, TIMESTAMP: str(int(time.time())), })
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


def client_sign(bduss, kw, fid, tbs):
    # 客户端签到
    data = copy.copy(SIGN_DATA)
    data.update({BDUSS: bduss, FID: fid, KW: kw, TBS: tbs, TIMESTAMP: str(int(time.time()))})
    data = encodeData(data)
    try:
        res = requests.post(url=SIGN_URL, data=data, timeout=1).json()
        return res
    except Exception:
        return None


def check(bduss):
    # 检查bduss是否失效
    headers = copy.copy(HEADERS)
    headers.update({COOKIE: EMPTY_STR.join([BDUSS, EQUAL, bduss])})
    return requests.get(url=TBS_URL, headers=headers).json()[IS_LOGIN]


if __name__ == '__main__':
    bduss = 'Y0U0dvVXhyTng3eFhhTzZ1bTVQUEhPc29DajZsaWpZa0hwR35NckQ1SWpPelJkSVFBQUFBJCQAAAAAAAAAAAEAAAC~0QE4x-u90M7SssrJq18AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACOuDF0jrgxdbn'
    name = get_name(bduss)
    print(name)
