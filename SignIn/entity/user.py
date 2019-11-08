# -*- coding:utf-8 -*-
from SignIn.utils.utils import get_tbs


class User(object):

    def __init__(self, id: int, bduss: str, username: str, token: str, flag: int):
        self.id = id
        self.bduss = bduss
        self.username = username
        self.token = token
        self.flag = flag
        self.tbs = self._get_tbs()
        self.tiebas = None

    def __str__(self):
        return "_".join([str(self.id), self.username])

    def set_tiebas(self, tiebas: list):
        self.tiebas = tiebas

    def sign(self):
        pass

    def update_like(self):
        pass

    def _get_tbs(self):
        return get_tbs(self.bduss)
