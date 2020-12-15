#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from json import dumps, loads
# --------   for python 2
# from httplib import HTTPConnection
# -----------    for python 3
from http.client import HTTPConnection

# connect with REST server
connection = HTTPConnection('127.0.0.1', 80)
connection.connect()

# MAKE HTTP REQUEST
connection.request(
    'POST',
    '/add_list_of_commands',
    dumps({"ip": "192.168.2.254"}),
    {'Content-Type': 'application/json'},
)
print("Waiting for Server response:")
result = loads(connection.getresponse().read())
print(result)


# close the connection
connection.close()