# -*- coding:utf-8 -*-

from SignIn.utils.utils import client_sign


class Tieba(object):

    def __init__(self, id: int, name: str, fid: int, is_sign: bool, status: str, user_id: int):
        self.id = id
        self.name = name
        self.fid = fid
        self.is_sign = is_sign
        self.status = status
        self.user_id = user_id

    def sign_one(self, bduss: str, tbs: str):
        client_sign(bduss=bduss, kw=self.name, fid=self.fid, tbs=tbs)

    def sign_one_callback(self, obj):
        print(obj.result())
