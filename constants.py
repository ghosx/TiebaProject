# -*- coding：utf8 -*-
from TiebaProject.settings import DATABASES

# API_STATUS
API_STATUS = {
    '0': '签到成功',
    '1': '用户未登录或登录失败，请更换账号或重试',
    '160002': '已经签过到了',
    '340008': '在黑名单中',
    '340006': '贴吧目录出问题啦',
    '300003': '加载数据失败',
    '3250001': '您的帐号涉及违规操作，现已被贴吧官方系统封禁',
    '1990055': '帐号未实名，功能禁用',
    '3250013': '您的账号封禁正在申诉中，暂不能进行此操作',
}

# SQL
## USER

SQL_GET_USER = "select id,bduss,username,token,flag from signin_user where flag = {} order by id ASC"
SQL_GET_ALL_USER = "select id,bduss,username,token,flag from signin_user order by id ASC"

### Tieba
GET_ALL_TIEBA = "select * from signin_sign where user_id = {} and is_sign = 0 order by id ASC"

# CLIENT_PARAMETER
SIMPLE_PARA = {
    '_client_type': '2',
    '_client_id': 'wappc_1534235498291_488',
    '_client_version': '9.7.8.0',
    '_phone_imei': '000000000000000',
    'from': '1008621y',
    'page_size': '200',
    'model': 'MI+5',
    'net_type': '1',
    'vcode_tag': '11',
}

# API_URL

LIKIE_URL = "http://c.tieba.baidu.com/c/f/forum/like"
TBS_URL = "http://tieba.baidu.com/dc/common/tbs"
SIGN_URL = "http://c.tieba.baidu.com/c/c/forum/sign"
GET_USERNAME_URL = "https://tieba.baidu.com/mo/q-"
FID_URL = "http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname={}"
QRCODE_URL = "https://passport.baidu.com/v2/api/getqrcode?lp=pc&apiver=v3&tpl=netdisk"
PASSPORT_URL = "https://passport.baidu.com/channel/unicast?channel_id={}&callback=&tpl=netdisk&apiver=v3"
LOGIN_URL = 'https://passport.baidu.com/v3/login/main/qrbdusslogin?bduss={}&u=https%253A%252F%252Fpan.baidu.com%252Fdisk%252Fhome&loginVersion=v4&qrcode=1&tpl=netdisk&apiver=v3&traceid=&callback=%27'

# HEADERS
QR_CODE_HEADER = {
    'Connection': 'keep-alive',
    'Host': 'passport.baidu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}


HEADERS = {
    'Host': 'tieba.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
}

SIGN_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ka=open',
    'User-Agent': 'bdtb for Android 9.7.8.0',
    'Connection': 'close',
    'Accept-Encoding': 'gzip',
    'Host': 'c.tieba.baidu.com',
}
SIGN_DATA = {
    '_client_type': '2',
    '_client_version': '9.7.8.0',
    '_phone_imei': '000000000000000',
    'model': 'MI+5',
    "net_type": "1",
}

# VARIABLE NAME
ERROR_CODE = "error_code"
FORM_LIST = "forum_list"
GCONFORM = "gconforum"
NON_GCONFORM = "non-gconforum"
HAS_MORE = "has_more"
ID = "id"
NAME = "name"
COOKIE = "Cookie"
BDUSS = "BDUSS"
CHANNEL_V = "channel_v"
EQUAL = r'='
EMPTY_STR = r''
TBS = 'tbs'
PAGE_NO = 'page_no'
ONE = '1'
TIMESTAMP = "timestamp"
DATA = 'data'
FID = 'fid'
SIGN_KEY = 'tiebaclient!!!'
UTF8 = "utf-8"
SIGN = "sign"
KW = "kw"
IS_LOGIN = "is_login"

# DATABASE

HOST = DATABASES['default']['HOST']
PORT = DATABASES['default']['PORT']
PASSWORD = DATABASES['default']['PASSWORD']
USER = DATABASES['default']['USER']
NAME = DATABASES['default']['NAME']

PYMYSQL_CONFIG = {
    'host': HOST,
    'port': PORT,
    'user': USER,
    'password': PASSWORD,
    'db': NAME,
    'charset': 'utf8',
}

# REGEX
USERNAME_REGEX = ">([\u4e00-\u9fa5a-zA-Z0-9_]+)的i贴吧<"
