#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from Module.UserAcc import UserAccSever
from Module.Comment import CommentSever
from Module.Weibo import WeiboSever
import json



def text(request):
    """
        查询我的关注
    :param request:
    :return:
    """
    # 查询我关注的人
    # user_id = 1
    # obj = UserAccSever().find_gz(user_id)
    # print(type(obj), obj)

    # from Repository.UserAcc import UserAcc
    # UserAcc().gz_my(1)

    ret = {'status': False, 'data': '', 'error': '', 'summary': '', "pic_id": ''}
    # if request.method == "GET":
    #     weibo_id = request.GET.get("weibo_id")
    #     obj_list = CommentSever().find_comment(weibo_id)
    #     obj_list = list(obj_list)
    #     for item in obj_list:
    #         item["date"] = str(item["date"])
    #     ret["status"] = True
    #     ret["data"] = json.dumps(obj_list)
    import datetime
    ti = datetime.datetime.now()
    comment = {"to_weibo_id": 195, "user_id": 1, "comment_type": 0, "comment": "我是好人!!!", "p_comment": None, "date": ti}


    from Module.Comment import CommentSever

    obj = CommentSever().comment_weibo(**comment)
    print(obj)

    return HttpResponse(json.dumps(ret))