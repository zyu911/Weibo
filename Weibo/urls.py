"""Weibo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web.controllers import account
from web.home import home
from web.controllers import text

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', account.user_login),
    url(r'^my_index/', account.my_index),
    url(r'^register/', account.register),
    url(r'^CheckCodeHandler/', account.CheckCodeHandler),

    url(r'^index/', home.index),
    url(r'^publish/', home.publish),
    url(r'^file/', home.upload_file),
    url(r'^home/', home.home),
    url(r'^find_text/', home.find_text),
    url(r'^auto/', home.auto),
    url(r'^comment/', home.comment),  # 获取评论
    url(r'^thumb_add/', home.thumb_add),  # 点赞
    url(r'^comment_weibo/', home.comment_weibo),  # 点赞


    url(r'^text/', text.text),
]
