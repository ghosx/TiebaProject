from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
import pymysql
import time
from SignIn.entity.user import User
from SignIn.entity.tieba import Tieba

from constants import PYMYSQL_CONFIG, SQL_GET_ALL_USER


def main():
    db = pymysql.connect(**PYMYSQL_CONFIG)
    db.autocommit(1)

    with db.cursor() as cur:
        cur.execute(SQL_GET_ALL_USER)
        users = cur.fetchall()
    user_objs = [User(*user) for user in users]

    pool = ProcessPoolExecutor(10)

    for user_obj in user_objs:
        pass






if __name__ == '__main__':
    t1 = time.time()
    main()
