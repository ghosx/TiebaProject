from TiebaProject.settings import *
import gevent
from gevent import monkey
from gevent.pool import Pool
from gevent.queue import Queue
monkey.patch_all()
import time
import requests
import pymysql
import hashlib

HOST = DATABASES['default']['HOST']
PORT = DATABASES['default']['PORT']
PASSWORD = DATABASES['default']['PASSWORD']
USER = DATABASES['default']['USER']
NAME = DATABASES['default']['NAME']

db = pymysql.connect(HOST, USER, PASSWORD, NAME)
db.autocommit(1)
cursor = db.cursor()

# 签到
sign_queue = Queue()
# 更新
update_queue = Queue()
# 检查BDUSS
check_queue = Queue()
# 云回
post_success_queue = Queue()
post_fail_queue = Queue()
post_data_queue = Queue()
# 所有的tbs
tbss = {}

DATA = {
    '0': '签到成功',
    '160002': '已经签过到了',
    '340008': '在黑名单中',
    '340006': '贴吧目录出问题啦',
    '300003': '加载数据失败',
    '3250001': '您的帐号涉及违规操作，现已被贴吧官方系统封禁',
    '1990055': '帐号未实名，功能禁用',
    '1': '用户未登录或登录失败，请更换账号或重试',
    '3250013': '您的账号封禁正在申诉中，暂不能进行此操作',
}


def getFliterUser(flag):
    sql = "select * from YunHui_user where flag = %s" % flag
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def getContent():
    sql = "select * from YunHui_content WHERE id >= (SELECT floor(RAND() * (SELECT MAX(id) FROM `YunHui_content`)))  ORDER BY id LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchone()
    return results[1]

def getYunHuiTiezi():
    sql = "select YunHui_tieba.id,bduss,fid,tid,name,isLou,floor,qid,time,success,stop,stop_times from YunHui_user,YunHui_tieba where YunHui_tieba.user_id = YunHui_user.id"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getUsers():
    sql = "select * from YunHui_user"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getTiebas(userid):
    sql = "select * from YunHui_sign where user_id = {} and is_sign = 0".format(userid)
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def getTBS(bduss):
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    try:
        res = requests.get(url=url, headers=headers, timeout=2).json()['tbs']
        return res
    except Exception:
        return None


def encodeData(data):
    SIGN_KEY = 'tiebaclient!!!'
    s = ''
    keys = data.keys()
    for i in sorted(keys):
        s += i + '=' + str(data[i])
    sign = hashlib.md5((s + SIGN_KEY).encode('utf-8')).hexdigest().upper()
    data.update({'sign': str(sign)})
    return data


def check_bduss_one(userid, bduss):
    # 功能函数
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    try:
        res = requests.get(url=url, headers=headers, timeout=2).json()['is_login']
        if res == 0 or res == '0':
            check_queue.put(userid)
    except Exception:
        pass


def add_tbs_to_tbss(userid, bduss):
    global tbss
    tbs = getTBS(bduss)
    tbss[userid] = tbs

def get_all_tbs():
    global tbss
    pool = Pool(20)
    users = getUsers()
    for user in users:
        userid = user[0]
        bduss = user[1]
        pool.add(gevent.spawn(add_tbs_to_tbss, userid, bduss))
    pool.join()
    print('all tbs end')

def client_LZL(Tieziid,bduss, kw, fid, content, quote_id, tid):
    # 客户端楼中楼
    tbs = getTBS(bduss)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.7.8.0',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }

    data = {
            'BDUSS':bduss,
            '_client_type':'2',
            '_client_id':'wappc_1534235498291_488',
            '_client_version':'9.7.8.0',
            '_phone_imei':'000000000000000',
            'anonymous':'1',
            'content':content,
            'fid':fid,
            'kw':kw,
            'model':'MI+5',
            'net_type':'1',
            'new_vcode':'1',
            'post_from':'3',
            'quote_id':quote_id,
            'tbs':tbs,
            'tid':tid,
            'timestamp':str(int(time.time())),
            'vcode_tag':'12',
        }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/c/post/add'
    try:
        res = requests.post(url=url, data=data, headers=headers, timeout=2).json()
        if res['error_code'] == '0':
            post_success_queue.put((Tieziid))
            post_data_queue.put((1))
        else:
            post_fail_queue.put((Tieziid))
    except Exception as e:
        print(e)

def client_Post(Tieziid,bduss, kw, tid, fid, content):
    # 客户端回帖模式
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.7.8.0',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }

    data = {
        'BDUSS':bduss,
        '_client_type':'2',
        '_client_version':'9.7.8.0',
        '_phone_imei':'000000000000000',
        'anonymous':'1',
        'content':content,
        'fid':fid,
        'from':'1008621x',
        'is_ad':'0',
        'kw':kw,
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
    try:
        res = requests.post(url=url, data=data, headers=headers, timeout=2).json()
        if res['error_code'] == '0':
            post_success_queue.put((Tieziid))
            post_data_queue.put((1))
        else:
            post_fail_queue.put((Tieziid))
    except Exception as e:
        print(e)

def sign_one(userid, bduss, kw, fid, tbs):
    # 客户端签到
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.7.8.0',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }
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
    url = 'http://c.tieba.baidu.com/c/c/forum/sign'
    try:
        res = requests.post(url=url, data=data, headers=headers).json()
        if str(res['error_code']) in DATA:
            sign_queue.put((userid, fid))
        elif str(res['error_code']) == '340011':
            # 签到频繁了
            gevent.sleep(1)
    except Exception as e:
        print(e)

def update_one(userid, bduss):
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
    try:
        res = requests.post(url=url, data=data, timeout=2).json()
    except Exception:
        return None
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
        try:
            url = 'http://c.tieba.baidu.com/c/f/forum/like'
            res = requests.post(url=url, data=data, timeout=2).json()
        except Exception:
            return None
        if 'non-gconforum' in res['forum_list']:
            returnData['forum_list']['non-gconforum'].append(res['forum_list']['non-gconforum'])
        if 'gconforum' in res['forum_list']:
            returnData['forum_list']['gconforum'].append(res['forum_list']['gconforum'])
    for x in returnData['forum_list']['non-gconforum']:
        if type(x) == list and x != []:
            for j in x:
                update_queue.put((j['id'], j['name'], j['level_id'], j['cur_score'], userid, j['id'], userid))
        else:
            update_queue.put((x['id'], x['name'], x['level_id'], x['cur_score'], userid, x['id'], userid))
    for y in returnData['forum_list']['gconforum']:
        if type(y) == list and y != []:
            for q in y:
                update_queue.put((q['id'], q['name'], q['level_id'], q['cur_score'], userid, q['id'], userid))
        else:
            update_queue.put((y['id'], y['name'], y['level_id'], y['cur_score'], userid, y['id'], userid))
    return returnData



##########################################################################################################################

def do():
    pool = Pool(10)
    tiezis = getYunHuiTiezi()
    stop_queue = Queue()
    content = getContent()
    sql1 = r"update YunHui_tieba set stop_times = stop_times + 1 where id = %s"
    sql2 = r"update YunHui_tieba set success = success + 1 where id = %s"
    sql3 = r"update YunHui_tieba set fail = fail + 1 where id = %s"
    sql4 = r"update YunHui_data set success = success + 1 where id = %s"
    for i in tiezis:
        ltime = time.localtime()
        t = ltime.tm_hour * 60 + ltime.tm_min
        if t % i[8] == 0:
            if i[10]:
                stop_queue.put((i[0]))
            else:
                if i[5]:
                    # Tieziid,bduss, kw, fid, content, quote_id, tid
                    pool.add(gevent.spawn(client_LZL,i[0],i[4],i[2],content,i[7],i[3]))
                else:
                    # Tieziid,bduss, kw, tid, fid, content
                    pool.add(gevent.spawn(client_Post,i[0],i[1],i[4],i[3],i[2],content))
    pool.join()
    to_mysql(stop_queue, sql1)
    to_mysql(post_success_queue, sql2)
    to_mysql(post_fail_queue,sql3)
    to_mysql(post_data_queue,sql4)


def newUpdate():
    sql = r"INSERT INTO YunHui_sign (`fid`,`name`,`level_id`,`cur_score`,`is_sign`,`user_id`) SELECT * from (select %s,%s, %s, %s,0,%s) as tmp WHERE NOT exists (select fid,user_id from YunHui_sign where fid = %s and user_id = %s) LIMIT 1"
    sql2 = r"update YunHui_user set flag = 1 where id = %s"
    db.autocommit(True)
    pool = Pool(20)
    userlist = Queue()
    # 未更新关注列表
    users = getFliterUser(0)
    if users == ():
        return 1
    for user in users:
        username = user[2]
        print(username)
        userid = user[0]
        userlist.put(userid)
        bduss = user[1]
        pool.add(gevent.spawn(update_one, userid, bduss))
    pool.join()
    to_mysql(update_queue, sql)
    to_mysql(userlist, sql2)


def newSign():
    pool = Pool(20)
    userlist = Queue()
    sql = r"update YunHui_sign set `is_sign` = 1 where user_id = %s and fid = %s"
    sql2 = r"update YunHui_user set flag = 2 where id = %s"
    users = getFliterUser(1)
    for user in users:
        bduss = user[1]
        tbs = getTBS(bduss)
        userid = user[0]
        userlist.put(userid)
        tiebas = getTiebas(user[0])
        for tieba in tiebas:
            print(tieba[1])
            pool.add(gevent.spawn(sign_one, userid, bduss, tieba[1], tieba[2], tbs))
    pool.join()
    to_mysql(sign_queue, sql)
    to_mysql(userlist, sql2)


def updata():
    pool = Pool(20)
    sql = r"INSERT INTO YunHui_sign (`fid`,`name`,`level_id`,`cur_score`,`is_sign`,`user_id`) SELECT * from (select %s,%s, %s, %s,1,%s) as tmp WHERE NOT exists (select fid,user_id from YunHui_sign where fid = %s and user_id = %s) LIMIT 1"
    users = getUsers()
    for user in users:
        username = user[2]
        print(username)
        userid = user[0]
        bduss = user[1]
        pool.add(gevent.spawn(update_one, userid, bduss))
    pool.join()
    to_mysql(update_queue, sql)


def sign():
    # 签到主函数
    pool = Pool(20)
    global tbss
    sql = "update YunHui_sign set is_sign = 1 where user_id = %s and fid = %s"
    # 获取所有的tbs
    get_all_tbs()
    users = getUsers()
    for user in users:
        userid = user[0]
        bduss = user[1]
        tbs = tbss[userid]
        tiebas = getTiebas(user[0])
        for tieba in tiebas:
            print(tieba)
            pool.add(gevent.spawn(sign_one, userid, bduss, tieba[1], tieba[2], tbs))
    pool.join()
    to_mysql(sign_queue, sql)


def to_mysql(queue, sql):
    print("to mysql start")
    while not queue.empty():
        item = queue.get()
        print(item)
        try:
            cursor.execute(sql, item)
        except Exception:
            db.rollback()
    print('to mysql end')


def check_bduss():
    # 检查bduss是否失效
    pool = Pool(20)
    users = getUsers()
    sql1 = "delete from YunHui_user where id = %s"
    sql2 = "delete from YunHui_sign where user_id = %s"
    sql3 = "delete from YunHui_tieba where user_id = %s"
    for user in users:
        userid = user[0]
        bduss = user[1]
        pool.add(gevent.spawn(check_bduss_one, userid, bduss))
    pool.join()
    to_mysql(check_queue, sql1)
    to_mysql(check_queue, sql2)
    to_mysql(check_queue, sql3)


def reset():
    # 每日重置签到
    sql = "update YunHui_sign set is_sign = 0"
    try:
        cursor.execute(sql)
    except Exception:
        db.rollback()

def clear_sign():
    # 清空签到表
    sql = "TRUNCATE TABLE YunHui_sign"
    try:
        cursor.execute(sql)
    except Exception:
        db.rollback()





