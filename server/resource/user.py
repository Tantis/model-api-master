from flask_restplus import Resource, Api
from .. import api

ns = api.namespace('user', description="用户信息")

class User(Resource):
    def get(self):
        "获取用户信息"
        return {}

    def post(self):
        "修改用户信息"
        
        payload = request.json
        
        introduction = payload["introduction"]
        dictionary_type = payload["dictionary_type"]
        image = payload["image"]
        if not isinstance(image, list):
            image = list(image)
        if not isinstance(image, list):
            return {"status": 400, "msg": "图片传递错误"}
        

ns.add_resource(User, '/')
