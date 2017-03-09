from flask_restplus import Resource, Api
from .. import api
from server.operation.register import Register
from server import db
from flask import request

import time

ns = api.namespace('opeartion', description="用户留言")


class Opeartion(Resource):
    """
    用户留言模块


    """

    def get(self):
        """
        随机查看一条留言

        """
        try:
            data = db.query_one(
                "SELECT content, FROM_UNIXTIME(create_time, '%Y-%m-%d %h') as create_time FROM `work_msg` ORDER BY RAND() DESC LIMIT 0, 1")

            return {'status': 200, 'msg': data}
        except Exception as err:
            return {'status': 400, 'msg': '失败'}

    def post(self):
        "用户留言模块"
        try:
            kwords = request.json
        except Exception as err:

            return {'status': 400, 'msg': '失败，你的数据格式不对 %s' % err}
        if not kwords:
            return {'status': 400, 'msg': '失败，你的数据格式不对'}
        kwargs = {}
        try:
            kwargs['msg'] = kwords['msg']
            kwargs['mobile'] = kwords['mobile']
            kwargs['name'] = kwords['name']
        except Exception as e:
            return {'status': 400, 'msg': '失败，你的数据格式不对 %s ' % e}
        kwargs['create_time'] = int(time.time())

        result = db.insert("""
        insert into 
        work_msg (mobile, name, content, create_time)
        value (:mobile, :name, :msg, :create_time)
        """, kwargs)
        if result:
            return {'status': 200, 'msg': '成功'}
        return {'status': 400, 'msg': '失败，你的数据格式不对'}

class OpeartionAll(Resource):
    def get(self):
        "获取用户所有留言"
        try:
            data = db.query(
                "SELECT content, FROM_UNIXTIME(create_time, '%Y-%m-%d %h') as create_time FROM `work_msg` ORDER BY id DESC")

            return {'status': 200, 'msg': data}
        except Exception as err:
            return {'status': 400, 'msg': '失败'}

ns.add_resource(Opeartion, '/')
ns.add_resource(OpeartionAll, '/all/')