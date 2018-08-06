from . import utils
from .models import User
import requests
import logging
import time

# 定时任务 设置在setting.py

def do():
    u = User.objects.all()
    content = requests.get('https://api.gushi.ci/rensheng.txt').text
    for i in u:
        ltime = time.localtime()
        t = ltime.tm_hour*60 + ltime.tm_min
        for j in i.tieba_set.all():
            if t % j.time == 0:
                if j.stop:
                    j.stop_times = j.stop_times + 1
                    j.save()
                    continue
                else:
                    if j.isLou:
                        try:
                            res = utils.LouZhongLou(i.bduss, content, j.name, j.fid, j.tid, j.qid, j.floor)
                            if res['err_code'] == 0:
                                j.success = j.success + 1
                            else:
                                j.fail = j.fail + 1
                        except Exception as e:
                            logging.info(e)
                        finally:
                            j.save()
                    else:
                        try:
                            ser = utils.HuiTie(i.bduss, content, j.tid, j.fid, j.name)
                            if ser['err_code'] == 0:
                                j.success = j.success + 1
                            else:
                                j.fail = j.fail + 1
                        except Exception as e:
                            logging.info(e)
                        finally:
                            j.save()