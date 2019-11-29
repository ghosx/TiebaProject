import os
import sys

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_path)

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TiebaProject.settings')
import django

django.setup()

from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time

from SignIn.models import User, Sign


def main():
    like = Queue()  # 更新关注队列
    sign = Queue()  # 签到队列
    thread_pool = ThreadPoolExecutor(max_workers=5)  # 初始化线程池数量

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
        else:
            print(time.time(), "empty like queue")

        while not sign.empty():
            s = sign.get()
            print(time.time(), "sign queue get:", s)
            if isinstance(s, Sign):
                thread_pool.submit(s.sign).add_done_callback(s.sign_callback)
        else:
            print(time.time(), "empty sign queue")

        time.sleep(5)


if __name__ == '__main__':
    main()
