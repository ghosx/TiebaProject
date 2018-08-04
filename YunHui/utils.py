import requests
import re
from bs4 import BeautifulSoup
import json

def getTBS(bduss):
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url=url,headers=headers).json()['tbs']

def getNameReplyAtByBduss(bduss):
    headers = {
        'Host':'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS='+bduss,
    }
    url = 'https://tieba.baidu.com/mo/q-'
    try:
        r = requests.get(url=url, headers=headers).text
        name = re.search(r">([\u4e00-\u9fa5a-zA-Z0-9]+)的i贴吧<", r).group(1)
        reply = re.search(r"回复我的\((\d+)\)", r).group(1)
        at = re.search(r"@我的\((\d+)\)", r).group(1)
    except Exception:
        name,reply,at = None,None,None
    finally:
        return name,reply,at

def getFavorite(bduss,stoken):
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss+';STOKEN='+stoken,
    }
    url = 'http://tieba.baidu.com/f/like/mylike'
    a = []
    res = requests.get(url=url,headers=headers).text
    weiye = int(re.search(r'pn=(\d+)">尾页',res).group(1))
    for i in range(1,weiye+1):
        print(i)
        url = url+'?&pn='+str(i)
        soup = BeautifulSoup(requests.get(url,headers=headers).text, 'html.parser').find('table').find_all('tr')[1:]
        for j in soup:
            tbname = j.find('a')['title']
            tbfid = getFid(tbname)
            tbjingyan = j.find(attrs={'class':'cur_exp'}).string
            tbdengji = j.find(attrs={'class':'like_badge_lv'}).string
            a.append((tbname,tbfid,tbjingyan,tbdengji,))
    print(a)
    return a



def getFid(bdname):
    url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname='+str(bdname)
    fid = requests.get(url).json()['data']['fid']
    return fid

def getDengji(bduss,bdname):
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/f?kw='+str(bdname)+'&ie=utf-8'
    print(url)
    print(headers)
    res = requests.get(url=url,headers=headers).text
    print(res)
    return res



def HuiTie(bduss,content,tid,fid,tbname):
    tbs = getTBS(bduss)
    headers = {
        'Accept':"application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding':"gzip, deflate, br",
        'Accept-Language':"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Connection':"keep-alive",
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': 'BDUSS='+bduss,
        'DNT':'1',
        'Host':'tieba.baidu.com',
        'Origin': 'https://tieba.baidu.com',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'ie':'utf-8',
        'kw':tbname,
        'fid':fid,
        'tid':tid,
        'tbs':tbs,
        '__type__':'reply',
        'content':content,
    }
    url = 'https://tieba.baidu.com/f/commit/post/add'
    r = requests.post(url=url,data=data,headers=headers).json()
    print(r)
    return r

def FaTie(bduss,title,content,tbname):
    fid = getFid(tbname)
    tbs = getTBS(bduss)
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': 'BDUSS=' + bduss,
        'DNT': '1',
        'Host': 'tieba.baidu.com',
        'Origin': 'https://tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'ie': 'utf-8',
        'kw': tbname,
        'fid': fid,
        'tbs': tbs,
        'title':title,
        '__type__': 'reply',
        'content': content,
    }
    url = 'https://tieba.baidu.com/f/commit/thread/add'
    r = requests.post(url=url, data=data, headers=headers).json()
    return r

def getQid(tid,floor):
    floor = int(floor)
    print('floor='+str(floor))
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    page = floor // 20 + 1
    print('page='+str(page))
    url = 'https://tieba.baidu.com/p/'+str(tid)+'?pn='+str(page)
    res = requests.get(url=url,headers=headers).text
    qid = re.findall(r"post_content_(\d+)",res)
    print(qid)
    try:
        return qid[floor-1]
    except Exception:
        return qid[len(qid)-1]

def LouZhongLou(bduss,content,tbname,fid,tid,qid,floor):
    tbs = getTBS(bduss)
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': 'BDUSS=' + bduss,
        'DNT': '1',
        'Host': 'tieba.baidu.com',
        'Origin': 'https://tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'ie': 'utf-8',
        'kw': tbname,
        'fid': fid,
        'tid': tid,
        'tbs': tbs,
        'quote_id':qid,
        'floor_num':floor,
        'content': content,
    }
    print(data)
    url = 'https://tieba.baidu.com/f/commit/post/add'
    r = requests.post(url=url, data=data, headers=headers).json()
    print(r)
    return r

#
bduss = 'VBmfmxkbFZEMWFaZ2xtQ1VPM35EZDhJeXZTajNhckVpWmlsWWF4M1NxVzM5b2xiQVFBQUFBJCQAAAAAAAAAAAEAAAC12ZM617fDzrXEt8XFo83eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALdpYlu3aWJbL'
content = "亲爱的我喜欢你"


# LouZhongLou(bduss,content,tbname,tid,qid)
# HuiTie(bduss,content,tid,fid,tbname)
