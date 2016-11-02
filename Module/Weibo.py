#! /usr/bin/env python
# -*- coding: utf-8 -*-
from Repository.Weibo import Weibo
from Module.UserAcc import UserAccSever


class IWeibo:
    pass


class WeiboSever:
    def __init__(self, repository=Weibo()):
        self.repository = repository

    def create_weibo(self, **kwargs):
        return self.repository.create_weibo(**kwargs)

    def weibo_page(self):
        return self.repository.weibo_page()

    def find_text(self, *text):
        obj = self.repository.find_text(*text)
        return obj

    def my_weibo(self, nid):
        """
            跟椐用户id查找其微博和自已的微博
        :param nid:
        :return:
        """
        li = list([nid])
        str_li = UserAccSever().find_gz(nid)  # 查询其关注人的微博
        for i in str_li:
            li.append(int(i))

        obj = self.repository.my_weibo(*li)

        return obj
