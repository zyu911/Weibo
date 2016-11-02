#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    发布微博
"""
import pika
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weibo.settings")
import django
django.setup()
from Repository import models
from Infrastructure.Rabbit.push import Push
import json
import shutil
from Infrastructure import Commons
from Weibo.settings import BASE_DIR


class WeiboPush:

    __obj = None

    def __init__(self, routing_key):
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='114.215.128.25'))
        self.channel = self.connection.channel()
        self.queue_name = None

    def bind(self, exchange='direct_logs'):
        self.channel.exchange_declare(exchange='direct_logs', type='direct')

        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue

        if isinstance(self.routing_key, list):
            for i in self.routing_key:
                self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key=i)
        else:
            self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key=self.routing_key)

    def callback(self, ch, method, properties, body):
        """
            收到消息后,将消息存入数据库,并发给调度都队列进行广播
            {'pictures_link_id': '1', 'wb_type': '1', 'user_id': 1, 'perm': 0, 'video_link_id': '', 'text': '顶替'}
        """
        body = json.loads(str(body, encoding='utf-8'))
        print("接收到任务 %s" % body)
        routing_key = body['user_id']
        path = body['user_id']
        print("发布信息关键字", routing_key)
        obj = models.Weibo.objects.create(**body)  # 存入数据库

        if obj and body["pictures_link_id"]:
            new_dir = Commons.my_md5(str(obj.id))
            user_dir = Commons.my_md5(str(obj.user_id))

            base_dir = os.path.join(BASE_DIR, "Statics", "upload", user_dir, new_dir)
            os.mkdir(base_dir)  # 新建当前微博Id对应的图片目录
            base_old_dir = os.path.join(BASE_DIR, "Statics", "upload", user_dir, 'temp')

            for i in os.listdir(base_old_dir):  # 移动文件到该目录
                shutil.move(os.path.join(base_old_dir, i), base_dir)

        body = json.dumps(body)

        Push().push(str(routing_key), body)   # 将发布人的 id 做为关健字推送

        # 清空用户当前临时目录
        path = Commons.my_md5(str(path))
        file_path = os.path.join(BASE_DIR, "Statics", "upload", path, 'temp')
        files = os.listdir(file_path)  # 清空目录内容
        for i in files:
            os.remove(os.path.join(file_path, i))
        print("清空文件夹")

        print("存库完成并分发")

    def start(self):

        self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)
        self.channel.start_consuming()


obj = WeiboPush('weibo')
obj.bind()
obj.start()





