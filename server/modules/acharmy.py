# -*- coding:utf-8 -*-

# Copyright (c) 2017 yu.liu <showmove@qq.com>
# All rights reserved


"""简化数据库操作


"""


class Search(object):
    """搜索服务


    """

    @classmethod
    def query(self, fields="*", table=None, where=()):
        """查询数据
        
        :parmas where:
             where[0] = ":is_deleted=:is_deleted or `status` in (SELECT x FROM Y WHERE I =:i )"
             where[1] = {"is_deleted": 0, "i": 2}

        """
        # qury = ",".join(["%s=:%s" % (i, i) for i in data])
        qur = "SELECT %(fields)s FROM %(table)s %(where)s" % {
            "fields": fields,
            "table" : table,
            "where" : " where " + where[0] if where[0] else ""
        }
        return db.query(qur)

class Modify(object):
    """操作和修改服务

    只针对拼接SQL语句

    """

    # 定义基本层级
    wcount = 0        

    @classmethod
    def update(self, table, where=(), data={}):
        """更新数据设置
        
        :parmas where:
             where[0] = ":is_deleted=:is_deleted or `status` in (SELECT x FROM Y WHERE I =:i )"
             where[1] = {"is_deleted": 0, "i": 2}
        :params data: 

            {
                "key": "value"

            }
        """
        upr = ",".join(["%s=:%s" % (i, i) for i in data])
        

        update = "UPDATE %(table)s SET %(upr)s %(where)s" % {"table": table, "upr": upr, "where": " where " + where[0] if where[0] else ""}

        # 检查条件
        data.update(where[1])
        
        return update

    @classmethod
    def insert(self, table, data):
        
        reprs = str(tuple(i for i in data.keys())).replace(",)", ")").replace("'", '`').replace('"', '`')
        value = str(tuple(":%s" % i for i in data.keys())).replace(",)", ")").replace("'", '').replace('"', '')
        return "INSERT INTO %(table)s %(reprs)s VALUES %(value)s" % {"table":table, "reprs":reprs, "value": value}
  



if __name__ == "__main__":
    print(Modify.update( table="user", where=("is_deleted=:is_deleted", {"is_deleted": 0}), data={"name": "b"}))

    print(Modify.insert("user", data={"name": "b", 'www': "v", "x": "y"}))
    print(Search.query(fields="*", table="logger",  where=("is_deleted=:is_deleted", {"is_deleted": 0})) )