from flask_restplus import Resource, Api
from .. import api
from server.operation.register import Register


import server.event as event
import server.operation as operation
import server.document as document

ns = api.namespace('RestoreList', description="列表")

class ExportRestoreList(Resource):
    
    """列表模块


    """
    @document.request_search
    @event.Event.execute(name="restore", controler=operation.EventModelExport)
    def get():
        return {"test": ""}

ns.add_resource(ExportRestoreList, '/')
