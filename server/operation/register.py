from ..utils import build_restful_final_decorator_class_by_funcs
from ..utils import wapper


class Register(object):

    @staticmethod
    @wapper
    def post(ok, response):
        return response

