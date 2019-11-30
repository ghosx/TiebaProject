import datetime
import os
import sys

from constants import MAX_WORKER, TIME_SLEEP

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_path)

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TiebaProject.settings')
import django

django.setup()

from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time

from apscheduler.schedulers.background import BackgroundScheduler

from SignIn.models import User, Sign


def main():
    # 定时任务相关 （仅作状态更改，具体任务由下方while循环来做）
    scheduler = BackgroundScheduler()
    # 每24小时更新一次关注的贴吧
    scheduler.add_job(User.objects.re_update_like, 'cron', hour='20')
    # 每天0点0分重置贴吧的签到状态
    scheduler.add_job(Sign.objects.reset_sign_status, 'cron', hour='0,22')
    # 检查用户的bduss是否失效
    scheduler.add_job(User.objects.check_all_user_valid, 'cron', hour='16')
    scheduler.start()
    ############################################################################################
    # 后台任务 （签到和更新关注贴吧）
    like = Queue()  # 更新关注队列
    sign = Queue()  # 签到队列
    thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKER)  # 初始化线程池数量
    while True:
        person_like = User.objects.need_update_like()
        for person in person_like:
            like.put(person)
            print(time.time(), "like queue put:", person)
        # 修改标记位，标记已经开始更新关注的贴吧
        User.objects.set_status_liking()

        signs = Sign.objects.need_sign()
        for s in signs:
            sign.put(s)
            print(time.time(), "sign queue put:", s)
        # 修改状态位 标记全部开始签到
        Sign.objects.set_status_signing()

        ################################################################

        while not like.empty():
            person = like.get()
            print(time.time(), "like queue get:", person)
            if isinstance(person, User):
                thread_pool.submit(person.like).add_done_callback(person.like_callback)

        while not sign.empty():
            s = sign.get()
            print(time.time(), "sign queue get:", s)
            if isinstance(s, Sign):
                thread_pool.submit(s.sign).add_done_callback(s.sign_callback)

        time.sleep(TIME_SLEEP)


if __name__ == '__main__':
    main()
