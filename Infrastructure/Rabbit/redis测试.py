#! /usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import json

pool = redis.ConnectionPool(host='114.215.128.25', port=6379)
r = redis.Redis(connection_pool=pool)

# r.set('1', '')
r.set('fao', 'xxoo')

print(r.get("1"))