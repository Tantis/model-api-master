from flask_restplus import Resource, Api
from .. import api
from server import db
from flask import request
from ..utils import *
import time
import requests


ns = api.namespace('login', description="用户登录")

class WXLogin(Resource):
    
    """用户登录模块


    """
    def get(self):
        "获取用户OPEN_ID"
        url = "https://api.weixin.qq.com/sns/jscode2session"
        data = {"appid": "wx54f787deee071681",
                "secret": "9c80f2830511ae9eacd47b9b396c8b62",
                "grant_type": "authorization_code"
        }
        r = requests.get(url, params=data)
        if r.status_code == 200:
            data = r.json()
            # 
            data['']


    # APPID      wx54f787deee071681
    # APPSECURE  9c80f2830511ae9eacd47b9b396c8b62
    def post(self):
        "通过WX登录后调用"
        kw = request.json
        try:
            user = {}
            user["user_id"] = kw['openid']
            # 检查用户是否已经存在数据
            result = db.query_one("SELECT * FROM user_profiles WHERE user_id=:user_id", user)
            if not result:
                # 添加用户
                user["gender"]  = kw["gender"]
                user["province"] = kw["province"]
                user["city"] = kw['city']
                user["login_time"] = int(time.time())
                user["status"] = 0
                user["avatar_url"] = kw["avatar_url"]
                result = db.insert(
                    """insert into user_profiles (`user_id`, `gender`, `province`, `city`, `login_time`, `status`, `avatar_url`)
                       values (:user_id, :gender, :province, :city, :login_time, :status, :avatar_url)
                    """, user
                    )

                return {"statuc": 200, 'msg': "成功"} 

            else:
                # 检查状态是否允许登录
                if result["status"] == 1:
                    return {"statuc": 401, 'msg': "不要再尝试挑战规则了。"}

                data = {}
                data["login_time"] = int(time.time())
                data["user_id"] = result["user_id"]
                result = db.update(
                    "UPDATE user_profiles SET login_time=:login_time WHERE user_id=:user_id", data
                )
                return {"statuc": 200, 'msg': "成功"}     
        except Exception as err:
            return {"statuc": 400, 'msg': err}

    def put(self):
        "短信登录"
        return {}

    def delete(self):
        "登出"

        return {}


ns.add_resource(WXLogin, '/')
