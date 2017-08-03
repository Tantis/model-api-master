from flask_restplus import Api, Resource

import server.document as document
from server.operation.register import Register

from .. import api
from server.utils.handler import _parent_resoves
ns = api.namespace('register', description="用户注册")

class Register(Resource):
    
    """用户注册模块


    """
    @document.DocumentFormart.request_model(data={"args1": 400, "args2": "成功"})
    @document.DocumentFormart.response_code(data={"status": 100006, "msg": "成功"}, code=400.1)
    @document.DocumentFormart.response_code(data={"status": 400, "msg": "成功"}, code=400)
    @document.DocumentFormart.response_code(data={"status": 200, "msg": "成功"}, code=200)
    def post(self):
        "用户注册"
        return _parent_resoves()


ns.add_resource(Register, '/')
