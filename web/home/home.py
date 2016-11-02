#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
import pika
from Infrastructure import Commons
from Weibo.settings import BASE_DIR
from Module.Weibo import WeiboSever
from Module.Comment import CommentSever
from Module.UserAcc import UserAccSever
import os
import redis
import json
import datetime


def comment_weibo(request):
    """
        增加评论
    :param request:
    :return:
    """
    ret = {'status': False, 'data': '', 'error': '', 'summary': '', "pic_id": ''}

    ti = datetime.datetime.now()
    comment = {"to_weibo_id": 195, "user_id": 1, "comment_type": 0, "comment": "", "p_comment": None, "date": ti}

    if request.session.get("is_login"):

        comment['to_weibo_id'] = request.POST.get("to_weibo_id")
        comment['comment'] = request.POST.get("comment")
        comment['p_comment'] = request.POST.get("p_comment")
        comment["user_id"] = request.session.get("user").get("id")
        print(comment)
        try:
            obj = CommentSever().comment_weibo(**comment)
            print(type(obj), obj, "-----------------------")

            obj_list = CommentSever().find_comment(comment["to_weibo_id"])
            obj = list(obj_list)[-1]
            obj["date"] = str(obj["date"])
            ret["status"] = True
            print(obj)
            ret["data"] = json.dumps(obj)

            # data["date"] = str(obj["date"])
            # ret["status"] = True
            # ret["data"] = json.dumps(obj_list)

            ret["status"] = True
            print("发布评论成功!!!")
        except Exception as E:
            ret["summary"] = str(E)
    else:
        ret["summary"] = "先登录"

    return HttpResponse(json.dumps(ret))


def thumb_add(request):
    ret = {'status': False, 'data': '', 'error': '', 'summary': '', "pic_id": ''}
    if request.session.get("is_login"):

        if request.method == "POST":
            weibo_id = request.POST.get("weibo_id")
            user_id = request.session.get("user").get("id")
            print(weibo_id, user_id)
            if weibo_id and user_id:
                try:
                    ti = datetime.datetime.now()
                    obj = CommentSever().comment_weibo(to_weibo_id=int(weibo_id), user_id=user_id, comment_type=1, date=ti)
                    ret["status"] = True
                except Exception as E:
                    print(str(E))
                    ret["status"] = False
            else:
                ret["status"] = False

    return HttpResponse(json.dumps(ret))


def comment(request):
    ret = {'status': False, 'data': '', 'error': '', 'summary': '', "pic_id": ''}
    if request.method == "POST":
        weibo_id = request.POST.get("weibo_id")
        obj_list = CommentSever().find_comment(weibo_id)
        obj_list = list(obj_list)
        for item in obj_list:
            item["date"] = str(item["date"])
        ret["status"] = True
        ret["data"] = json.dumps(obj_list)

    return HttpResponse(json.dumps(ret))


def auto(request):
    ret = {'status': False, 'data': '', 'error': '', 'summary': '', "pic_id": ''}
    if request.method == "POST":

        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)

        user_id = request.session.get("_auth_user_id", 1)

        data = r.get(user_id)
        print(data, "!!!!!!")
        if data:
            data = json.loads(str(data, encoding="utf-8"))
            r.set(user_id, "")
            print("查询到最新 %s 条信息", data.get("count", None))

            ret["data"] = str(data.get("count", None))
            ret["status"] = True
        else:
            ret["status"] = False

    return HttpResponse(json.dumps(ret))


def upload_file(request):
    """
        上传图片
    :param request:
    :return:
    """
    ret = {'status': False, 'data': '', 'error': '', 'summary': '', "pic_id": ''}
    if request.session.get("is_login"):
        path = request.session.get("user").get("id")
        path = Commons.my_md5(str(path))

        # file_path = os.path.join(BASE_DIR, "Statics", "upload", path, 'temp')
        # files = os.listdir(file_path)  # 清空目录内容
        # for i in files:
        #     os.remove(os.path.join(file_path, i))

        if request.method == "POST":
            obj = request.FILES.getlist('fafafa')
            for file in obj:

                file_path = os.path.join(BASE_DIR, "Statics", "upload", str(path), 'temp',
                                         "%s.%s" % (Commons.generate_md5(file.name), file.name.split(".")[-1]))
                print(file_path)
                f = open(file_path, 'wb')
                for chunk in file.chunks():
                    f.write(chunk)
                f.close()
            ret["pic_id"] = 1
            ret["status"] = True

            return HttpResponse(json.dumps(ret))


def publish(request):
    """
        发布微博
    :param request:
    :return:
    """
    ret = {'status': False, 'data': '', 'error': '', 'summary': ''}

    data = {"user_id": 1, "text": "我是内容", "pictures_link_id": 1, "video_link_id": 1, "perm": 0, "wb_type": 0}

    if request.session.get("is_login", True):

        if request.method == "POST":
            data['user_id'] = request.session.get("user").get("id")  # !! _auth_user_id
            data['text'] = request.POST.get("text", None)
            data['pictures_link_id'] = request.POST.get("pictures_link_id", None)
            data['video_link_id'] = request.POST.get("video_link_id", None)
            data['perm'] = request.POST.get("perm", 0)
            data['wb_type'] = request.POST.get("wb_type", 0)

            if data['pictures_link_id']:
                data['pictures_link_id'] = Commons.my_md5(str(data["user_id"]))
            print(data, '浏览器发过来的数据')

            try:
                # 发布数据
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=''))  # 建立连接
                channel = connection.channel()  # 获得句柄
                channel.exchange_declare(exchange='direct_logs',  # 交换机名(除非重起,否则不可变)
                                         type='direct')  # 类型为关分侵字发布
                severity = 'weibo'  # 向关健字发布
                message = json.dumps(data)  # 发布内容
                channel.basic_publish(exchange='direct_logs',
                                      routing_key=severity,
                                      body=message)
                pri = "发布的内容 %r:%r" % (severity, message)
                print(pri)
                connection.close()
                ret["status"] = True
                ret["summary"] = "发送成功!"
            except Exception as E:
                ret["summary"] = str(E) + "放入队列错误,发布失败!"
    else:
        ret["summary"] = "先登录"

    return HttpResponse(json.dumps(ret))


def index(request):

    obj = WeiboSever().weibo_page()  # 查询所有微博
    data_list = []

    for i in obj:
        data = {}
        comment_num = CommentSever().find_comment(i.id)  # 查询评论数
        comment_num = len(list(comment_num))
        thumb_num = CommentSever().comment_thumb_up(i.id)  # 查询点赞数
        data["pic_list"] = []
        if i.pictures_link_id:
            print("有图片", i.user_id, i.id)
            user_dir_name = Commons.my_md5(str(i.user_id))
            weibo_dir_name = Commons.my_md5(str(i.id))
            pic_list = os.path.join(BASE_DIR, "Statics", "upload", user_dir_name, weibo_dir_name)
            for pic_src in os.listdir(pic_list):
                src = "/statics/upload/%s/%s/%s" % (user_dir_name, weibo_dir_name, pic_src)
                data['pic_list'].append(src)

        data['weibo'] = i
        data['comment_num'] = comment_num if comment_num else 0
        data['thumb_num'] = thumb_num if comment_num else 0
        data_list.append(data)
        print(data)
    for i in data_list:
        print(i)

    return render(request, 'home/index.html', {"data_list": data_list, "request": request})


def home(request):
    """
        个人主页只显示我发布的微博和我关注的人的策博
    :param request:
    :return:
    """
    if request.session.get("is_login", None):

        user_id = int(request.session.get("user").get("id"))
        obj = WeiboSever().my_weibo(user_id)
        gz_my = UserAccSever().gz_my(user_id)
        gz_my = len(list(gz_my))
        print("我关注的人%s" % gz_my)
        my_gz = UserAccSever().find_gz(user_id)  # 查询我关注的人
        my_gz = len(my_gz)

        data_list = []

        for i in obj:
            data = {}
            comment_num = CommentSever().find_comment(i.id)
            comment_num = len(list(comment_num))
            thumb_num = CommentSever().comment_thumb_up(i.id)
            data["pic_list"] = []
            try:
                if i.pictures_link_id:
                    print("有图片", i.user_id, i.id)
                    user_dir_name = Commons.my_md5(str(i.user_id))
                    weibo_dir_name = Commons.my_md5(str(i.id))
                    pic_list = os.path.join(BASE_DIR, "Statics", "upload", user_dir_name, weibo_dir_name)
                    for pic_src in os.listdir(pic_list):
                        src = "/statics/upload/%s/%s/%s" % (user_dir_name, weibo_dir_name, pic_src)
                        data['pic_list'].append(src)
            except Exception as E:
                data["pic_list"] = []
                print("系统打不到指定的路径 用户id: %s 微博id: %s" % (i.user_id, i.id))

            data['weibo'] = i
            data['comment_num'] = comment_num if comment_num else 0
            data['thumb_num'] = thumb_num if thumb_num else 0
            data_list.append(data)
            print(data)
        for i in data_list:
            print(i)

        return render(request, 'home/home.html', {"data_list": data_list, "request": request, "gz_my": gz_my, "my_gz": my_gz})

    else:
        return redirect("/index/")


def find_text(request):
    text = request.GET.get("text")
    text = text.split(" ")
    print(text)
    obj = WeiboSever().find_text(*text)

    data_list = []

    for i in obj:
        data = {}
        comment_num = CommentSever().find_comment(i.id)
        thumb_num = CommentSever().comment_thumb_up(i.id)
        data["pic_list"] = []
        if i.pictures_link_id:
            print("有图片", i.user_id, i.id)
            user_dir_name = Commons.my_md5(str(i.user_id))
            weibo_dir_name = Commons.my_md5(str(i.id))
            pic_list = os.path.join(BASE_DIR, "Statics", "upload", user_dir_name, weibo_dir_name)
            for pic_src in os.listdir(pic_list):
                src = "/statics/upload/%s/%s/%s" % (user_dir_name, weibo_dir_name, pic_src)
                data['pic_list'].append(src)

        data['weibo'] = i
        data['comment_num'] = comment_num
        data['thumb_num'] = thumb_num
        data_list.append(data)
        print(data)
    for i in data_list:
        print(i)

    return render(request, 'home/find.html', {"data_list": data_list, "request": request})


