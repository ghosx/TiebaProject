from concurrent.futures import ThreadPoolExecutor
import requests
import pymysql
import time

from constants import PYMYSQL_CONFIG

not_sigined_user = []
not_sync_like_user = []

db = pymysql.connect(**PYMYSQL_CONFIG)
db.autocommit(1)
cursor = db.cursor()

if __name__ == '__main__':
    t1 = time.time()
    pool = ThreadPoolExecutor(10)
    for url in urls:
        pool.submit(get, url).add_done_callback(parse)
    t2 = time.time()

    print(t2 - t1)
