from flask_restplus import Resource, Api
from .. import api

ns = api.namespace('user', description="用户信息")

class User(Resource):
    def get(self):
        "获取用户信息"
        return {}

    def post(self):
        "修改用户信息"
        return {}


ns.add_resource(User, '/')
