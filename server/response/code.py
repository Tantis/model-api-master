#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved

"""定制错误代码

RESPONSE CODE:
    SUCCESS = 200
    FAILDS  = 400
"""
class Default(object):
    
    # 成功
    Success = 200
    
    # 失败
    Failed  = 400
    
    # 参数失败
    ArgsError = 403
    
    # 资源为空
    NotFound = 404    

    # 服务器内部错误
    InternalServerError = 500

    # 登录信息有误
    Unlogin = 401

    

class DefaultStatus(object):
    
    Decriptions = {
        Default.Success: '成功',
        Default.Failed:  '失败',
        Default.NotFound: '未找到该资源',
        Default.ArgsError: '请求参数有误',
        Default.InternalServerError: '服务器内部错误',
        Default.Unlogin: '登录信息有误'
    }    

    

class Login(Default):
    pass

class Register(Default):
    pass

class Information(Default):
    pass


def build_result(status, data=None):
    if data:
        return {'status': status, 'msg': DefaultStatus.Decriptions[status], 'data': data}
    return {'status': status, 'msg': DefaultStatus.Decriptions[status]}