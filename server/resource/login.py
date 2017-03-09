from flask_restplus import Resource, Api
from .. import api
from server import db
from flask import request
from ..utils import *


ns = api.namespace('login', description="用户登录")

class Login(Resource):
    """用户登录模块


    """
    
    def post(self):
        "密码登录"
        return True, request.json


    def put(self):
        "短信登录"
        return {}

    def delete(self):
        "登出"

        return {}


ns.add_resource(Login, '/')
