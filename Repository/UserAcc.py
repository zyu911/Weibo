#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import models


class UserAcc:

    def find_user(self, user_id):
        """查询一位用户详细"""
        obj = models.UserProfile.objects.filter(user_id=user_id).values("id", "name", "email", "head_img", 'age')
        print(obj)
        return obj

    def create_user(self, **kwargs):
        """
        新建一位用户 返回
        {username: "xiao", password: "abcdefgh", email: "abce@qq.com"}
        """
        user = models.User.objects.create_user(**kwargs)
        obj = models.UserProfile.objects.create(name='您的昵称',
                                                sex=1,
                                                email=kwargs["email"],
                                                head_img="1.jpg",
                                                user_id=user.id)

        return obj

    def find_gz(self, nid):
        """
            查询我的关注
        :param nid:
        :return:  我关注的人的id列表(内为字符串)
        """
        li = []
        obj = models.UserProfile.objects.filter(follow_list=nid)
        for i in obj:
            li.append(str(i.id))

        return li

    def gz_my(self, nid):
        """
            查询关注我的人
        :param nid:
        :return:   关注我的人的数量(数字)
        """
        obj = models.UserProfile.objects.filter(follow_list__id=nid)
        print("ghdalkdflkadflajsdfl!!!!!!!!!!!!!!!!!!!!")
        for i in obj:
            print(type(obj), i.name)
        return obj
