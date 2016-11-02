#! /usr/bin/env python
# -*- coding: utf-8 -*-
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# import redis
#
# r = redis.Redis(host='114.215.128.25', port=6379)
# # r.set('foo', 'Bar', nx=10)
# b = r.get('foo')
# # print([bin(i) for i in b])
# ok = r.getbit('foo', 7)
# print(ok)
# print(r.keys())
# print(r.get('index'))


import redis
import json

pool = redis.ConnectionPool(host='', port=6379)
r = redis.Redis(connection_pool=pool)

r.set('zyu', 'yu')
# r.set('fao', 'xxoo')

print(r.get("zyu"))

a = r.get('1')
r.set('1', '')
print(a)
# if a:
#     print("True")
#     s = json.loads(str(a, encoding='utf-8'))
#     print(s)
# else:
#     print("False")