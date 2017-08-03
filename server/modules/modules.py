#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved


class model(dict):
    """简洁版MODEL
    => conf = model()
    => conf = {'dd': {'cc': {'ee': {'xx' : 'test'}}}}, {'a': 'b'}
    => print(conf.dd.cc.ee.xx)
    ```
    test
    ```
    """

    def __init__(self, *args, **kwarg):
        """MODULES
        :PARAMS ARGS :
        :PARAMS KWARG:
        :RETURN : OBJECTDICT
        """
        super().__init__(*args, **kwarg)

        for __attrbute in self.keys():
            setattr(self, __attrbute, self[__attrbute])

    def __values_to_model(self, value):

        if isinstance(value, (list, tuple, set)):
            _aval = []
            for _val in value:
                if isinstance(_val, dict):
                    _val = model(_val)
                elif isinstance(_val, (list, tuple, set)):
                    _val = self.__values_to_model(_val)
                _aval.append(_val)

            _aval = value.__class__(_aval)
            return _aval

        elif isinstance(value, dict):
            value = model(value)

        return value

    def __setattr__(self, key, value):

        try:

            if not hasattr(self, key):
                self[key] = value
                value = self.__values_to_model(value)
        except Exception as e:
            print(type(key), value)
            raise(e)

        super().__setattr__(key, value)

    def __getattr__(self, key):
        return super().__getattr__(self, key)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        elif key in self.keys():
            return self.get(key)
        else:
            return super().__getitem__(key)

    def __getattribute__(self, *args, **kwargs):

        return object.__getattribute__(self, *args, **kwargs)



if __name__ == "__main__":
    dicts = {'dd': {'cc': {'ee': {'xx': 'test'}}}}
    z = model(dicts)
    print(z.dd.cc.ee.xx)