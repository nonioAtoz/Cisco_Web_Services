#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from json import dumps, loads
# for python 2
# from httplib import HTTPConnection
# for python 3
from http.client import HTTPConnection

# connect with REST server
connection = HTTPConnection('127.0.0.1', 80)
connection.connect()

data = {"ip": "192.168.2.254",
        "list_of_commands_to_send": "show version"
        }

# Get the method response
connection.request(
    'POST',
    '/add_command_raw',
    dumps(data),
    {'Content-Type': 'application/json'},
)
print("Waiting for Server response:")

response = connection.getresponse()
code = response.getcode()
headers = response.getheaders()
result = loads(response.read())
print(result)
print("code: ", code)
print("headers: ", headers)
print(dir(result))

# close the connection
connection.close()