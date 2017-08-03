#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved

"""文档驱动模块

"""

import json
import uuid

from flask_restplus import fields

from server import api, db
from server.response.code import DefaultStatus, build_result
from flask_restplus.utils import merge


class NotDocumentError(Exception):
    pass


class DocumentFormart:

    __swich_fields_keys = {
        "str": fields.String,
        "int": fields.Integer,
        "float": fields.Float,
        "Decimal": fields.Arbitrary,
    }

    @classmethod
    def NestedList(self, data):
        """返回列表中的数据

        """
        _fileds = {}
        for _key in data:
            if isinstance(_key, dict):
                _fileds = self.NestedDict(_key)
        return _fileds

    @classmethod
    def NestedDict(self, data):
        """返回字典里面的数据

        """
        return self.ResponseBody(data, "", response_fileds=True)

    @classmethod
    def ResponseBody(self, data, model_name, response_model="model", response_code="200", response_data="成功", response_templates=None, response_fileds=False, function=None):
        """返回整个BODY
        :params data          : response data
        :params response_model: model | response
        :return : response data model
        """

        models = {}
        for _key in data:
            if isinstance(data[_key], dict):
                _fields = fields.Nested(model=api.model(
                    _key, self.NestedList(data[_key])))
            elif isinstance(data[_key], list):
                _fields = fields.List(fields.Nested(
                    model=api.model(_key, self.NestedList(data[_key]))))
            else:
                _fields = self.__swich_fields_keys[data[_key].__class__.__name__](
                    data[_key], Description=data[_key])
            models[_key] = _fields
        if response_fileds:
            return models
        if response_model == "response":
            return api.response(
                response_code, response_data, model=api.model(model_name, models))
        # if function:
        #     api.doc(body=api.model(model_name, models))(function)
        return api.doc(body=api.model(model_name, models))

    @classmethod
    def response_code(self, code="200", response_data="成功", name=None, data={}):
        if not name:
            name = str(uuid.uuid1()).replace("-", '')
        return self.ResponseBody(data, name, response_model="response", response_data=response_data, response_code=code)

    @classmethod
    def request_model(self, code=0, name=None, data={}, **kwarg):
        if not name:
            name = str(uuid.uuid1()).replace("-", '')
        return self.ResponseBody(data, name, response_model="model")

    @classmethod
    def request_param(self, name=None, data={}, **kwarg):
        
        return api.doc(params=data)


    @classmethod
    def register(self, doc_name="test_document", doc_type=0, doc_version="1.0.0"):

        document_data = db.query_one("SELECT * FROM `document_register` WHERE `name`=:name AND `type` = :type AND `version`=:version",
                                     {"name": doc_name, "type": doc_type,
                                         "version": doc_version}
                                     )

        if not document_data:
            raise(NotDocumentError("没有文档信息: %s" % doc_name))

        _document_type = {
            0: self.response_code,
            1: self.request_model
        }
        try:
            data = json.loads(document_data["data"])

            return _document_type[doc_type](code=document_data["code"], name=document_data["name"], data=data)
        except Exception as err:
            import ipdb
            ipdb.set_trace()

    @staticmethod
    def registerclass(cls):
        """使用类名查询数据库注册文档


        """
        document_data = db.query("SELECT * FROM `document_register` WHERE `name`=:name AND `version`=:version",
                                 {"name": cls.__name__, "version": cls.__version__})
        _document_type = {
            0: DocumentFormart.response_code,
            1: DocumentFormart.request_model,
            2: DocumentFormart.request_param
        }
        for item in document_data:
            if item["func"].upper() in cls.methods:
                data = json.loads(item["data"])
                _document_type[item["type"]](code=item["code"],
                                             name=item[
                                                 "name"] + item["func"] + str(item["type"]),
                                             response_data=item["response"],
                                             data=data)(getattr(cls, item["func"].lower()))
        return cls
