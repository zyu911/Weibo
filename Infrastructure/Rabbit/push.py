#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import json
from Repository.UserAcc import UserAcc


# 客户端用户登录用

class Push:

    def __init__(self, exchange='direct_logs'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='114.215.128.25'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange,  # 交换机名(除非重起,否则不可变)
                                      type='direct')  # 类型为关分侵字发布

    def push(self, severity, message):
        """
            :param severity: 向关健字发布
            :param message:  发布的内容
            :return:
        """
        self.channel.basic_publish(exchange='direct_logs',
                                   routing_key=severity,
                                   body=message)
        print("%r关键字发送:%r" % (severity, message))
        self.connection.close()


class UserPull:

    def __init__(self, routing_key, user_id):
        self.user_id = user_id
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
        self.channel = self.connection.channel()
        self.queue_name = None

        import redis
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.redis = redis.Redis(connection_pool=pool)

    def bind(self, exchange='direct_logs'):
        self.channel.exchange_declare(exchange='direct_logs', type='direct')

        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue

        if isinstance(self.routing_key, list):
            for i in self.routing_key:
                print(i, "被绑定")
                self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key=i)
        else:
            self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key=self.routing_key)

    def callback(self, ch, method, properties, body):
        """
        body为消息字典,数据单条记录  append 到消息记录中
        """
        body = json.loads(str(body, encoding='utf-8'))

        new = self.redis.get(self.user_id)  # 获取自己的id对应的消息
        if new:
            data = json.loads(str(new, encoding="utf-8"))
        else:
            data = {'user_id': self.user_id, "body": [], "count": 0}

        data['count'] += 1  # 消息数加 1
        data['body'].append(body)  # 传递消息,追加

        data_str = json.dumps(data)
        self.redis.set(self.user_id, data_str)  # 用自已的 id 设置 redis 保存消息
        print('看看存上没', json.loads(str(self.redis.get(self.user_id), encoding='utf-8')))

    def start(self):

        self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)
        self.channel.start_consuming()
