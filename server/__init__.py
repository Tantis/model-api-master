#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2015 yu.liu <showmove@qq.com>
# All rights reserved

"""
test

"""
import json

from flask import Blueprint, Flask, jsonify, url_for
from flask_restplus import Api

from server.db import MySQLdb
from server.modules import model

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api'
                    )
api = Api(blueprint, doc='/doc/',version='1.0', title='Sample API',
                      description='A sample API')

app.register_blueprint(blueprint)

# 读取配置文件
with open('jobs_config.json', 'r', encoding='utf8') as __conf:
    conf = json.load(__conf)

configs = model(conf)

db = MySQLdb(dict(configs.mysql.dev))






from server import index
from server import resource



@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    print(error)
    return {'status': 500, "msg": "服务器内部错误..", "message": ""}