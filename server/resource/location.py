from flask_restplus import Resource, Api
from .. import api
import server.document as document
import server.operation as operation
import server.event as event
ns = api.namespace('position', description="用户信息")


class Position(Resource):
    """


    """
    # 装饰方法
    # Event.execute
    # 分层管理概念， 层数等级自定义.
    @event.Event.execute(name="error_404", controler="make_error")
    @event.Event.execute(name="default", controler="make_response")
    @event.Event.execute(name="user", controler=operation.Register)
    def get():
        """ 获取当前用户的定位 """
        return {"ds": 400}
    @event.Event.execute(name="finger", controler=operation.Register)
    def post():
        """ 上传当前用户的定位 """
        return {"ds": 400}


ns.add_resource(Position, '/')
