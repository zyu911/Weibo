#! /usr/bin/env python
# -*- coding: utf-8 -*-
from web.Forms import Forms
from web.Forms.login_forms import LoginForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from Repository.models import *
import io
import json
import threading
from Repository.UserAcc import UserAcc
from Infrastructure.Rabbit.push import UserPull
from Module.UserAcc import UserAccSever
import os
from Infrastructure import Commons
from Weibo.settings import BASE_DIR
from Infrastructure.Code import check_code


def my_index(request):
    if request.session.get("is_login", None):
        return render(request, "account/my_index.html", {"request": request})
    else:
        return redirect("/index/")


def register(request):
    """用户注册"""
    ret = {"status": False, "data": {}, "error": {}, 'summary': ''}

    if request.method == "GET":
        return render(request, "account/register.html")

    elif request.method == "POST":
        try:
            kwargs = {"username": "zyu911", "password": "abcdefgh", "email": "abc@abc.com"}
            user = UserAccSever().create_user(**kwargs)

            user_dir_name = Commons.my_md5(str(user.user_id))
            user_path = os.path.join(BASE_DIR, "Statics", "upload", user_dir_name)
            os.mkdir(user_path)
            temp_path = os.path.join(user_path, "temp")
            os.mkdir(temp_path)

            ret["status"] = True
            request.session["is_login"] = True
            request.session["user"] = user
            print(request.session["is_login"], request.session["user"], "注册成功")
        except Exception as E:
            ret["error"] = str(E)

    return HttpResponse(json.dumps(ret))


def user_login(request):
    """用户登录"""

    ret = {"status": False, "data": {}, "error": {}, 'summary': ''}
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        # kwargs = {"username": "zyu911", "password": "abcdefgh", "email": "abc@abc.com"}
        # UserAccSever().create_user(**kwargs)

        print(username, password)
        print("ddd", Commons.my_md5(password))
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)  # 登录
                request.session["is_login"] = True
                ret['status'] = True
                obj = UserAccSever().find_user(request.session.get("_auth_user_id"))

                request.session["user"] = obj[0]
                # print(request.session['user']['name'], 'xxx登录')
                print(request.session.get("_auth_user_id"), "xxx用户登录!")

                obj = UserAccSever().find_gz(request.session["user"].get("id"))  # 查询本人关注的用户的id结果为列表
                print(type(obj), obj, "我关注的人的id ['1', '2', '3']  <------")

                if not request.session.get("thread", None):
                    print("起动线程")

                    li = ['1', '2', '3', "17"]  # 我的关注列表用于订阅   自已的id用于在redis中存取数据
                    obj = UserPull(obj, request.session.get("_auth_user_id"))
                    obj.bind()
                    t = threading.Thread(target=obj.start)
                    t.start()
                    request.session["thread"] = 1

    ret["error"] = {"user": "用户名或密码错误!"}

    return HttpResponse(json.dumps(ret))


def logout(request):
    print("logout,,,,ayu")
    request.session['is_login'] = False
    return redirect('/index/')


def CheckCodeHandler(request):
    stream = io.BytesIO()
    img, code = check_code.create_validate_code()
    img.save(stream, "png")
    request.session["CheckCode"] = code
    print(request.session["CheckCode"], '为什么要走这')
    return HttpResponse(stream.getvalue())
