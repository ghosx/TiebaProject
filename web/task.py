from constants import SIGN_WORKER, TIME_SLEEP, LIKE_WORKER
from apscheduler.schedulers.background import BackgroundScheduler
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import django
import os
import sys

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_path)

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TiebaProject.settings')
django.setup()

# 这里读取了setting配置，所以必须放在django.setup() 后面
from SignIn.models import User, Sign


def main():
    # 定时任务相关 （仅作状态更改，具体任务由下方while循环来做）
    scheduler = BackgroundScheduler()
    # 每10点更新一次关注的贴吧
    scheduler.add_job(User.objects.re_update_like, 'cron', hour='10')
    # 每天0点0分重置贴吧的签到状态，进行签到
    scheduler.add_job(Sign.objects.reset_sign_status, 'cron', hour='0')
    # 每天8,12,18点再次签到
    scheduler.add_job(Sign.objects.reset_sign_status_again, 'cron', hour='8,12,16')
    # 检查用户的bduss是否失效,并且邮件通知
    scheduler.add_job(User.objects.check_all_user_valid, 'cron', hour='9')
    scheduler.start()
    ############################################################################################
    # 后台任务 （签到和更新关注贴吧）
    like = Queue()  # 更新关注队列
    sign = Queue()  # 签到队列
    like_thread_pool = ThreadPoolExecutor(
        max_workers=LIKE_WORKER, thread_name_prefix="like_")  # 初始化线程池数量
    sign_thread_pool = ThreadPoolExecutor(
        max_workers=SIGN_WORKER, thread_name_prefix="sign_")  # 初始化线程池数量
    while True:
        person_like = User.objects.need_update_like()
        for person in person_like:
            like.put(person)
        # 修改标记位，标记已经开始更新关注的贴吧
        if not like.empty():
            User.objects.set_status_liking()

            while not like.empty():
                person = like.get()
                if isinstance(person, User):
                    like_thread_pool.submit(person.like).add_done_callback(
                        person.like_callback)
        # 上面是获取关注贴吧
        ################################################################
        # 下面是对贴吧进行签到
        signs = Sign.objects.need_sign()
        for s in signs:
            sign.put(s)
        # 修改状态位 标记全部开始签到
        if not sign.empty():
            Sign.objects.set_status_signing()

            while not sign.empty():
                s = sign.get()
                if isinstance(s, Sign):
                    sign_thread_pool.submit(
                        s.sign).add_done_callback(s.sign_callback)

        time.sleep(TIME_SLEEP)


if __name__ == '__main__':
    main()
