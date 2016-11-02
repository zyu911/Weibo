#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Count, Min, Max, Sum
from . import models


class Comment:
    def comment_weibo(self, **kwargs):
        """
            评论一条微博
        """
        print("增加评论------------>", kwargs)
        obj = models.Comment.objects.create(**kwargs)
        return obj

    def comment_thumb_up(self, nid):
        """
             根据id查询点赞数
        """
        obj = models.Comment.objects.filter(to_weibo_id=nid, comment_type=1).count()
        return obj

    def find_comment(self, nid):
        """
            根据微博id查询评论
        """
        obj = models.Comment.objects.filter(to_weibo_id=nid, comment_type=0).values("id",
                                                                                    "date",
                                                                                    "comment",
                                                                                    "user__name",
                                                                                    "p_comment__id")
        return obj
