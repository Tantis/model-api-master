#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved

"""装饰模块


"""
from server.response import *
from functools import wraps


def build_generator(func):
    """
    装饰器生成函数
    :param func:
    :return:
    """
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            return func(f, *args, **kwargs)
        return decorator
    return wrapper


def build_continuation_passing(func):
    """
    延续传递生成函数
    :param func:
    :return:
    """
    def wrapper(continuation, *args, **kwargs):
        ok, response = continuation(*args, **kwargs)
        if not ok:
            return ok, response
        return func(response)
    return wrapper

def build_final_continuation_passing(func):
    """
    filter延续传递生成函数
    :param func:
    :return:
    """
    def wrapper(continuation, *args, **kwargs):
        ok, response = continuation(*args, **kwargs)
        return func(ok, response)
    return wrapper


def build_restful_passing_decorator_class_by_funcs(name, methods):
    return type(name, (object, ),
           {func.__name__:
            build_generator(build_continuation_passing(func))
            for func in methods})

def build_restful_final_decorator_class_by_funcs(name, methods):
    return type(name, (object,),
           {func.__name__: build_generator(build_final_continuation_passing(func))
            for func in methods})


def wapper(f):
    """参数效验

    """
    def __install(**params):
        avatar = {}
        for _par in params:
            avatar[_par] = params[_par]

        def __decotors(func):
            @wraps(func)
            def __console(*args, **kwargs):

                ok, response = func(**kwargs)
                for item in response:
                    if item in avatar.keys():
                        if not isinstance(response[item], avatar[item]):
                            return f(False, build_result(Default.ArgsError))
                        continue
                return f(True, response)

            return __console
        return __decotors
    return __install
