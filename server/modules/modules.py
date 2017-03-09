#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved


class model(dict):
    """简洁版MODEL
    => conf = model()
    => conf = [{'dd': {'cc': {'ee': {'xx' : 'test'}}}}, {'a': 'b'}]
    => print(conf.dd.cc.ee.xx)
    ```
    test
    ```
    """
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        for __attrbute in self.keys():
            setattr(self, __attrbute, self[__attrbute])

    def __setattr__(self, key, value):
        try:
            if not hasattr(self, key):
                self[key] = value
                if isinstance(value, dict):
                    value = model(value)
                elif isinstance(value, list):
                    value = [model(i) for i in value]
                elif isinstance(value, tuple):
                    value = tuple([model[i] for i in value])
                else:
                    pass
        except Exception as e:
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


class WithOperations(object):

    name = ''
    def __init__(self, name):
        self.name = name
        self.value = []

    def __setattr__(self, key, val):
        if key not in ['name', 'value']:
            try:
                self.value.append(" `{0}` = '{1}'".format(key, "%(val)s" % {'val': val}))
            except Exception as e:
                raise(AttributeError)
        else:
            super().__setattr__(key, val)



class CursorReader(object):

    def __init__(self, name, primary_id='id'):
        self.name = name
        self.primary_id = primary_id

    def _or(self):
        pass


class CursorWriter(object):
    pass




if __name__ == "__main__":
    x = CursorReader('test')
    z = WithOperations('wd')
    z.index = 'aaa'

    print(z.value)
    conf = model({})
    conf.host = '127.0.0.1'
    conf.user = 'root'
    conf.password = 'dandanMIJIAN'
    conf.charset = 'utf8mb4'
    conf.db = 'wen10_cn'
    conf.cursorclass = cursors.DictCursor
    #conf.array = [{'dd': {'cc': {'ee': {'xx' : 'test'}}}}, {'a': 'b'}]
    #conf.word = {'aa': 'bb'}
    #conf.zz = [{'zz': 'xxx'}, {'uu': 'ww'}]
    #last_out_print(**conf)
    #import ipdb
    #ipdb.set_trace()
    #connection = connect(host=conf.host, user=conf.user, password=conf.password,
    #                      charset=conf.charset, db=conf.db,
    #                      cursorclass=conf.cursorclass)
    connection = connect(**conf)
    #with connection.cursor() as cursor:
    #    sql = "SELECT * FROM `base_food` limit 0, 100
    #    cursor.execute(sql)
    #    result = cursor.fetchall()#
    #    print(result)
    p = Connection(**conf)
    result = p.query_one('SELECT * FROM base_food')
    #result.id
    print(result.parentid)
    print(result.image)
    print(result.listorder)
