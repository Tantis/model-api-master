from flask_restplus import Resource, Api
from .. import api
from server import db
from flask import request
from ..utils import *
import time
import requests
import uuid

import server.event as event



class WXLogin(Resource):

    """用户登录模块


    """
    @event.Event.execute(name="user")
    def get():
        "获取用户OPEN_ID"
        tokens = request.args.get("token")
        if not tokens:
            return {"status": 404, "msg": '参数错误'}
        
        result = db.query_one("""
            SELECT * FROM tokens WHERE token=:token AND is_deleted=0 AND expiration_time >= :time
        """, {"token": tokens, "time": int(time.time())})
        if not result:
            return {"status": 401, "msg": 'token已过期'}
        return {"status": 200, "msg": "成功", "data": result["user_id"]}
    
    def post(self):
        "通过WX登录后调用"

        try:
            
            kw = request.json
            user = {}
            user["user_id"] = kw["user_id"]
            # 检查用户是否已经存在数据
            result = db.query_one(
                "SELECT * FROM user_profiles WHERE user_id=:user_id", user)
            if not result:
                # 添加用户
                user["nickname"] = kw["nickName"]
                user["gender"] = kw["gender"]
                user["province"] = kw["province"]
                user["city"] = kw["city"]
                user["login_time"] = int(time.time())
                user["status"] = 0
                user["avatar_url"] = kw["avatarUrl"]
                result = db.insert(
                    """insert into user_profiles (`user_id`, `nickname`, `gender`, `province`, `city`, `login_time`, `status`, `avatar_url`)
                       values (:user_id, :nickname, :gender, :province, :city, :login_time, :status, :avatar_url)
                    """, user
                )
                print({"statuc": 200, "msg": "成功"})
                return {"statuc": 200, "msg": "成功"}

            else:
                # 检查状态是否允许登录
                if result["status"] == 1:
                    return {"statuc": 401, "msg": "不要再尝试挑战规则了。"}

                data = {}
                data["login_time"] = int(time.time())
                data["user_id"] = result["user_id"]
                result = db.update(
                    "UPDATE user_profiles SET login_time=:login_time WHERE user_id=:user_id", data
                )
                print({"statuc": 200, "msg": "成功"})
                return {"statuc": 200, "msg": "成功"}
        except Exception as err:
            print(err);
            return {"statuc": 400, "msg": err}

    def put(self):
        "获取SESSION"
        try:
            param = request.json
            
            url = "https://api.weixin.qq.com/sns/jscode2session"
            data = {"appid": "wx54f787deee071681",
                    "secret": "9c80f2830511ae9eacd47b9b396c8b62",
                    "grant_type": "authorization_code",
                    "js_code": param["code"]
                    }
        except Exception as err:
            return {"status": 404, "msg": '失败'}

        r = requests.get(url, params=data)
        if r.status_code == 200:
            data = r.json()
            print(data)
            if not data.get("errcode"):
                user_id = data["openid"]
                db.update("UPDATE tokens SET is_deleted=1 WHERE user_id=:user_id", {"user_id": user_id})

                session_key = data["session_key"]
                token = str(uuid.uuid4()).replace('-', '')
                tokens = {
                    "user_id": user_id,
                    "token": token,
                    "device_id": "",
                    "expiration_time": int(time.time()) + 3600,
                    "create_time": int(time.time()),
                    "update_time": int(time.time()),
                    "is_deleted": 0,
                    "session_key": session_key
                }
                print(tokens)

                result = db.insert("""
                insert into `tokens`
                        (
                        `user_id`,
                        `token`,
                        `device_id`,
                        `expiration_time`,
                        `create_time`,
                        `update_time`,
                        `is_deleted`,
                        `session_key`)
                values (
                        :user_id,
                        :token,
                        :device_id,
                        :expiration_time,
                        :create_time,
                        :update_time,
                        :is_deleted,
                        :session_key);
                """, tokens)
                if not result:
                    return {"status": 404, "msg": '失败'}
                
                return {"status": 200, "msg": '成功', "token": tokens['token'], "user_id": user_id}

                
            else:
                print(data);
                return {"status": 401, "msg": data["errmsg"]}
        else:
            return {"status": 401, "msg": "失败"}
    def delete(self):
        "登出"
        return {}

class WXuserInfo(Resource):
    
    def get(self):
        "获取用户信息"
        tokens = request.args.get("token")
        if not tokens:
            return {"status": 404, "msg": '参数错误'}
        
        result = db.query_one("""
            SELECT * FROM tokens WHERE token=:token AND is_deleted=0 AND expiration_time >= :time
        """, {"token": tokens, "time": int(time.time())})
        if not result:
            return {"status": 401, "msg": 'token已过期'}
        result = db.query_one("""
        SELECT * FROM user_profiles WHERE user_id = :user_id        
        """, {"user_id": result["user_id"]})
        result["nickName"] = result["nickname"]
        result["avatarUrl"] = result["avatar_url"]
        return {"status": 200, "msg": "成功", "data": result}

ns = api.namespace("login", description="用户登录")
ns1 = api.namespace("info", description="用户信息")
ns.add_resource(WXLogin, '/')
ns1.add_resource(WXuserInfo, '/')