#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved

# pylint: disable-all

"""工具模块包


"""
# import lxml
from lxml.html.clean import Cleaner
import lxml.html as HTML
# import lxml.html.soupparser as HTML
from lxml.html import HtmlElement
from lxml.etree import XPathError, tostring
import requests
from html.parser import HTMLParser
import html

HTML_PARSER = HTMLParser()

Cleaner.safe_attrs_only = False
Cleaner.safe_attrs = False
Cleaner.annoying_tags = False
Cleaner.style = True
Cleaner.meta = False
Cleaner.page_structure = False
Cleaner.processing_instructions = False
Cleaner.embedded = False


class XPath(object):

    """XPath工具类，简化lxml操作。"""

    def __init__(self, content=None):
        """初始化

        :param content: 需要预编译的内容。
        """

        # TODO: Cleaner误杀实在太严重了
        #self.cleaner = Cleaner()
        # This is True because we want to activate the javascript filter
        #self.cleaner.scripts = clear_scripts
        #self.cleaner.javascript = clear_scripts

        if content is not None:
            if isinstance(content, HtmlElement):
                self._parser_content = content
            else:
                self.compile(content)

    def compile(self, content):
        """把内容预编译成xml树，加快xpath表达式运行。

        :param content: 需要预编译的内容，unicode文本。

        """

        self._parser_content = HTML.fromstring(content)

        # self._parser_content = self.cleaner.clean_html(
        #    HTML.document_fromstring(content))

    def execute(self, *arg, **kwargs):
        """运行XPath表达式。

        :param path: xpath表达式。
        :return: 返回结果列表，有可能是字符串或者XPath对象。例如：

                * ``//a/@href`` 返回一个包含所有a标签href属性的字符串列表
                * ``//div[@class='test']`` 返回一个 XPath 列表。
        """
        try:
            return [x.strip()
                    if isinstance(x, str)
                    else XPath(tostring(x))
                    for x in self._parser_content.xpath(*arg, **kwargs)]
            # return self._parser_content.xpath(*arg, **kwargs)

        except XPathError as err:
            print(err)
            return None

    def to_html(self):
        """返回html文本。"""
        return html.unescape(tostring(self._parser_content, pretty_print=True).decode('utf8', 'ignore'))

        # return HTML.tostring(self._parser_content)

    def to_text(self):
        """返回本节点文本内容,不包含子节点。"""
        return self._parser_content.text_content()


class Http:

    """
    网络请求

    """
    @staticmethod
    def get(cls, *args, **kwarg):
        """抓取装饰

        """

        def decoter(func, *args, **kwarg):
            """装饰详情

            """

            url, headers, data = cls(func)
            r = requests.get(url, headers=headers, params=data)
            if r.status_code == 200:
                return XPath(r.text)
            return
        return decoter

    @staticmethod
    def post(cls, *args, **kwarg):
        """抓取装饰

        """

        def decoter(*args, **kwarg):
            """装饰详情

            """
            url, hedaers, data = cls(func)
            r = requests.post(url, headers=headers, json=data)
            if r.status_code == 200:
                return XPath(r.text)
            return
        return decoter

    @staticmethod
    def put(cls, *args, **kwarg):
        """抓取装饰

        """

        def decoter(*args, **kwarg):
            """装饰详情

            """
            url, hedaers, data = cls()
            r = requests.put(url, headers=headers, data=data)
            if r.status_code == 200:
                return XPath(r.text)
            return
        return decoter


class Request(object):

    # 挖掘地址
    CUR_URL = "https://www.baidu.com"

    # 浏览器头部
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,' \
        'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh_CN',
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate'
    }

    # 代理IP, 数组形式
    PROXY = []

    # 设置超时时间
    TIMEOUT = 30

    

    @classmethod
    @Http.get
    def on_get_start(self, *args, **kwarg):

        return self.CUR_URL, self.HEADERS, {}

    @classmethod
    @Http.post
    def on_post_start(self, *args, **kwarg):

        return self.CUR_URL, self.HEADERS, {}

    @classmethod
    @Http.put
    def on_put_start(self, *args, **kwarg):

        return self.CUR_URL, self.HEADERS, {}

if __name__ == "__main__":

    Request.CUR_URL = "http://liuyu.info"
    Request.HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,' \
        'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh_CN',
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate'
    }
    result = Request.on_get_start()
    import ipdb
    ipdb.set_trace()
