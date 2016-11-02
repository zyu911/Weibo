#! /usr/bin/env python
# -*- coding: utf-8 -*-
from Repository.UserAcc import UserAcc


class IUserAcc:
    pass


class UserAccSever:
    def __init__(self, repository=UserAcc()):
        self.repository = repository

    def find_user(self, user_id):
        return self.repository.find_user(user_id)

    def create_user(self, **kwargs):
        return self.repository.create_user(**kwargs)

    def find_gz(self, nid):
        """
            查询我关注的人
        :param nid:
        :return:
        """
        return self.repository.find_gz(nid)

    def gz_my(self, nid):
        """
            查询关注我的人
        :param nid:
        :return:
        """
        return self.repository.gz_my(nid)
