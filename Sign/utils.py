import requests
import re
from bs4 import BeautifulSoup

def getTBS(bduss):
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url=url,headers=headers).json()['tbs']

def getUsernameByBduss(bduss):
    headers = {
        'Host':'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS='+bduss,
    }
    url = 'https://tieba.baidu.com/mo/q-'
    r = requests.get(url=url,headers=headers).text
    name =  re.search(r">([\u4e00-\u9fa5a-zA-Z0-9]+)的i贴吧<",r)
    if name is not None:
        name = name.group(1)
    else:
        name = 'anonymous'
    return name

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
        # if i == 2:
        #     break
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

def getStoken(bduss):
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'https://passport.baidu.com/v2/api/?getapi&apiver=v3'
    res = requests.get(url=url,headers=headers)
    print(res.status_code)


def getFid(bdname):
    url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname='+str(bdname)
    fid = requests.get(url).json()['data']['fid']
    # print(fid)
    return fid

# bduss = '1IxSXV5cUdHTEdmNGx5YWg5ZnY2eUpxUGZhdERzdGlMQX5IZzktWnI3ejM2b2RiQVFBQUFBJCQAAAAAAAAAAAEAAAC12ZM617fDzrXEt8XFo83eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPddYFv3XWBbM'
# stoken = 'e7f5d88e4f9128fe12a5b0d76f9ec21c59a006e1b720bf4dd83c14dd645ad5c1'

