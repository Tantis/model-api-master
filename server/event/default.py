#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved

"""默认控制器


"""

from flask import make_response
from flask import jsonify
from flask import abort

class EventFiltersMakeResponse(object):
    """
    默认的filter层

    主要提供make_response的一些默认response

    """
    @classmethod
    def default(cls, response):
        print(response)
        return make_response(jsonify(response), response["status"])
      


class EventFiltersControlResponse(object):
    """
    控制器返回层

    主要提供一些控制返回结果

    """
    pass


class EventErrorResponse(object):

    """
    控制器返回层

    主要提供一些失败控制返回结果

    """

    @classmethod
    def error_404(cls, response, msg="失败"):
        return make_response(jsonify({"status": 404, "msg": msg}), 404)

    @classmethod
    def error_401(cls, response, msg="认证失败"):
        return make_response(jsonify({"status": 401, "msg": msg}), 401)

    @classmethod
    def error_402(cls, response, msg="失败"):
        return make_response(jsonify({"status": 402, "msg": msg}), 402)

    @classmethod
    def error_403(cls, response, msg="失败"):
        return make_response(jsonify({"status": 403, "msg": msg}), 403)


class EventSuccessResponse(object):
    """
    控制器返回层

    主要提供一些成功控制返回结果

    """
    @classmethod
    def success_200(cls, response, msg="成功", data={}):
        return make_response(jsonify({"status": 200, "msg": msg, data: data}), 401)