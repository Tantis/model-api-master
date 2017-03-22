#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved


import time
import uuid

import requests
from flask import request
from flask_restplus import Api, Resource

from server import db

from .. import api
from ..utils import *


class ModelList(Resource):

    def get(self):
        "获取用户列表"
        where = request.args
        try:
            index = int(where.get("index", 0))
            count = 11
        except Exception as err:
            return {"status": 400, "msg": "错误"}, 400

        # 查询用户信息
        infoSql = "select * from `user_profiles` WHERE `status` !=1"
        result = db.query(infoSql)
        if not result:
            return {"status": 404, "msg": '没有数据'}
        # filters 状态 0=空闲 1=接单 2=停止接单 3=休息
        keys = {0: "空闲", 1: "接单", 2: "停止接单", 3: "休息"}

        for k, v in enumerate(result):
            # 每个用户只要查出一部视频信息

            videoSql = "SELECT * FROM `user_video` WHERE is_hide=0 AND is_deleted=0 AND user_id=:user_id ORDER BY create_time DESC limit 0, 1"
            video = db.query_one(videoSql, {"user_id": v["user_id"]})
            v["video"] = video

            # 判断当前用户的状态
            status = v["operation_state"]
            v["status"] = keys[status]

            result[k] = v

        return {"status": 200, "msg": "成功", "data": result}
ns = api.namespace('models', description="信息列表")
ns.add_resource(ModelList, "/")