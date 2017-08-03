#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved

"""事件驱动模块

主要用于层次管理
```

@Event.execute(name="user", controler=EventControl)
def func():
    return {"data": 123}

```

"""
import inspect


from .default import *

class Event(object):
    """
    事件驱动模块
    """
    @staticmethod
    def execute(name="default", controler=None):
        """装饰事件
        :params name    : 可选参数，如果不想默认使用相同方法！可指定方法
        :params control : 可选参数, 传递项要的事件控制器
        """
        def control(func): 
            swich_default = {
                "make_response": EventFiltersMakeResponse,      # 支持跨域访问 
                "make_coltrol" : EventFiltersControlResponse,   # 支持其他访问
                "make_error"   : EventErrorResponse,            # 返回错误
                "make_success" : EventSuccessResponse           # 返回成功
            }
            _controler = EventControl
            _name = name
            if controler:
                if inspect.isclass(controler):
                    _controler = controler
                elif isinstance(controler, str):
                    if controler in swich_default.keys():
                        _controler = swich_default[controler]
                    else:
                        # 开发人员写错控制器错误
                        _controler = EventErrorResponse
                        _name = "error_404"
            try:
                result = lambda x: getattr(_controler, _name)(x())
            except Exception as err:
                result = lambda x: getattr(EventErrorResponse, "error_404")(x())
            def __console(*args, **kwargs):
                # print(args, kwargs)
                return result(func)
            return __console
        return control

class EventControl(object):
    """事件驱动方法

    用户定义什么事件既可以使用什么事件
    """
    @classmethod
    def default(cls, response):
        # print(response)
        return response
