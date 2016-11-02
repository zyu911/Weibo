#! /usr/bin/env python
# -*- coding: utf-8 -*-
from Repository import models


class Weibo:
    def create_weibo(self, **kwargs):
        # 新建一篇微博
        # {'perm': 0, 'video_link_id': 1, 'pictures_link_id': 1, 'user_id': 1, 'text': '我是内容,我不是内容', 'wb_type': 0}
        obj = models.Weibo.objects.create(**kwargs)

        return obj

    def weibo_page(self, start=0, rows=9):
        """根据时间取前10条"""

        obj = models.Weibo.objects.all().order_by('-date')[start: rows]
        return obj

    def find_text(self, *text):
        obj = models.Weibo.objects.filter(text__contains=text[0])
        print(obj)
        return obj

    def my_weibo(self, *li):
        """
            查询我的微博和我关注的人的微博
        :param li: 我关注的人的列表
        :return:
        """
        obj = models.Weibo.objects.filter(user_id__in=li).order_by('-date')[0: 9]
        return obj
