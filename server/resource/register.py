from flask_restplus import Resource, Api
from .. import api
from server.operation.register import Register

ns = api.namespace('register', description="用户注册")

class Register(Resource):
    """用户注册模块


    """
    @staticmethod
    @Register.post(a=int, b=str)
    def post():
        "用户注册"
        return True, {'a': 123, 'b': 'c'}


ns.add_resource(Register, '/')
