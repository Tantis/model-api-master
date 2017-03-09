from flask_restplus import Resource, Api
from .. import api
from server.operation.register import Register
from server.modules.utils import Request as Crawler
from flask import request
ns = api.namespace('crawler', description="数据抓取")


class Crawlers(Resource):

    def get(self):
        try:
            url = request.args.get('url')
            Crawler.CUR_URL = url
            Crawler.HEADERS = {
                'Accept': 'text/html,application/xhtml+xml,'
                'application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh_CN',
                'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate'
            }
            result, response = Crawler.on_get_start()
            if result:
                section = [i.to_text().replace('\n', '')
                           for i in result.execute('//div')]
                return {'status': 200, 'msg': '成功', 'data': section}
            return {'status': 404, 'msg': '失败'}
        except Exception as err:
            return {'status': 404, 'msg': '失败, %s ' % err}


ns.add_resource(Crawlers, '/')
