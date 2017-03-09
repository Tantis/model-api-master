#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2015 yu.liu <showmove@qq.com>
# All rights reserved

"""
test

"""
import json
from flask import Flask, Blueprint
from flask import url_for
from flask_restplus import Api
from server.modules import model
from server.db import MySQLdb

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


