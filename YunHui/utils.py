import requests
import re
from bs4 import BeautifulSoup
import json

def getTBS(bduss):
    # 获取tbs
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url=url,headers=headers).json()['tbs']

def getNameReplyAtByBduss(bduss):
    # 获取贴吧用户名和at reply信息
    headers = {
        'Host':'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
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
    # 获取用户关注的贴吧
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
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
    # 获取贴吧对用的fourm id
    url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname='+str(bdname)
    fid = requests.get(url).json()['data']['fid']
    return fid

def getDengji(bduss,bdname):
    # 获取贴吧等级
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/f?kw='+str(bdname)+'&ie=utf-8'
    print(url)
    print(headers)
    res = requests.get(url=url,headers=headers).text
    print(res)
    return res



def HuiTie(bduss,content,tid,fid,tbname):
    # 网页版回帖
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
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
    print(r['err_code'])
    return r

def FaTie(bduss,title,content,tbname):
    # 网页版发帖
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
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
    print(r['err_code'])
    return r

def getQid(tid, floor):
    # 获取楼中楼的qid参数
    floor = int(floor)
    print('floor='+str(floor))
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
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

def getFname(tid):
    # 通过tid获取贴吧名字
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    url = 'https://tieba.baidu.com/p/' + str(tid)
    res = requests.get(url=url, headers=headers).text
    TBname = re.search("fname=\"([^\"]+)\"", res).group(1)
    print(TBname)
    return TBname


def LouZhongLou(bduss,content,tbname,fid,tid,qid,floor):
    # 网页端楼中楼
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
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
    url = 'https://tieba.baidu.com/f/commit/post/add'
    r = requests.post(url=url, data=data, headers=headers).json()
    print(r['err_code'])
    return r

def encodeData(data):
    SIGN_KEY = 'tiebaclient!!!'
    s = ''
    keys = data.keys()
    for i in sorted(keys):
        s += i + '=' + str(data[i])
    sign = hashlib.md5((s + SIGN_KEY).encode('utf-8')).hexdigest().upper()
    data.update({'sign': str(sign)})
    return data

def clientPost(bduss,tbname,tid,content):
    # 客户端回帖模式
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.3.8.5',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }

    data = {
        'BDUSS':bduss,
        '_client_type':'2',
        '_client_version':'9.3.8.5',
        '_phone_imei':'000000000000000',
        'anonymous':'1',
        'content':content,
        'fid':getFid(tbname),
        'from':'1008621x',
        'is_ad':'0',
        'kw':tbname,
        'model':'MI+5',
        'net_type':'1',
        'new_vcode':'1',
        'tbs':getTBS(bduss),
        'tid':tid,
        'timestamp':str(int(time.time())),
        'vcode_tag':'11',
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/c/post/add'
    a = requests.post(url=url,data=data,headers=headers)
    print(a.json())

#
if __name__ == '__main__':
   pass


