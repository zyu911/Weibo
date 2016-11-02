#! /usr/bin/env python
# -*- coding: utf-8 -*-
from Repository.Comment import Comment


class CommentSever:
    def __init__(self, comment=Comment()):
        self.comment = comment

    def comment_weibo(self, **kwargs):
        """
            评论一条微博
        """
        obj = self.comment.comment_weibo(**kwargs)
        return obj

    def comment_thumb_up(self, nid):
        """
             根据id查询点赞数
        """
        obj = self.comment.comment_thumb_up(nid)
        return obj

    def find_comment(self, nid):
        """
            根据微博id查询评论
        """
        obj = self.comment.find_comment(nid)
        return obj
