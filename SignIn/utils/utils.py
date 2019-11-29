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
    returnData = {}
    i = 1
    data = {
        'BDUSS': bduss,
        '_client_type': '2',
        '_client_id': 'wappc_1534235498291_488',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        'from': '1008621y',
        'page_no': '1',
        'page_size': '200',
        'model': 'MI+5',
        'net_type': '1',
        'timestamp': str(int(time.time())),
        'vcode_tag': '11',
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/f/forum/like'
    res = requests.post(url=url, data=data, timeout=2).json()
    returnData = res
    if 'forum_list' not in returnData:
        returnData['forum_list'] = []
    if res['forum_list'] == []:
        return {'gconforum': [], 'non-gconforum': []}
    if 'non-gconforum' not in returnData['forum_list']:
        returnData['forum_list']['non-gconforum'] = []
    if 'gconforum' not in returnData['forum_list']:
        returnData['forum_list']['gconforum'] = []
    while 'has_more' in res and res['has_more'] == '1':
        i = i + 1
        data = {
            'BDUSS': bduss,
            '_client_type': '2',
            '_client_id': 'wappc_1534235498291_488',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            'from': '1008621y',
            'page_no': str(i),
            'page_size': '200',
            'model': 'MI+5',
            'net_type': '1',
            'timestamp': str(int(time.time())),
            'vcode_tag': '11',
        }
        data = encodeData(data)
        url = 'http://c.tieba.baidu.com/c/f/forum/like'
        res = requests.post(url=url, data=data, timeout=2).json()
        if 'non-gconforum' in res['forum_list']:
            returnData['forum_list']['non-gconforum'].append(res['forum_list']['non-gconforum'])
        if 'gconforum' in res['forum_list']:
            returnData['forum_list']['gconforum'].append(res['forum_list']['gconforum'])

    t = []
    for i in returnData['forum_list']['non-gconforum']:
        if isinstance(i, list):
            for j in i:
                if isinstance(j, list):
                    for k in j:
                        t.append(k)
                else:
                    t.append(j)
        else:
            t.append(i)
    for i in returnData['forum_list']['gconforum']:
        if isinstance(i, list):
            for j in i:
                if isinstance(j, list):
                    for k in j:
                        t.append(k)
                else:
                    t.append(j)
        else:
            t.append(i)
    return t


def encodeData(data):
    s = EMPTY_STR
    keys = data.keys()
    for i in sorted(keys):
        s += i + EQUAL + str(data[i])
    sign = hashlib.md5((s + SIGN_KEY).encode(UTF8)).hexdigest().upper()
    data.update({SIGN: str(sign)})
    return data


def client_sign(bduss, sign):
    # 客户端签到
    data = copy.copy(SIGN_DATA)
    tbs = get_tbs(bduss)
    data.update({BDUSS: bduss, FID: sign.fid, KW: sign.name, TBS: tbs, TIMESTAMP: str(int(time.time()))})
    data = encodeData(data)
    res = requests.post(url=SIGN_URL, data=data, timeout=1).json()
    return res


if __name__ == '__main__':
    pass
