from server import db


class Operation(object):
    """
    操作驱动模块
    """

    @staticmethod
    def execute(name="user", controler=None):
        """装饰事件
        :params name    : 可选参数，如果不想默认使用相同方法！可指定方法
        :params control : 可选参数, 传递项要的事件控制器
        """
        def control(func):
            result = lambda x: getattr(OperationDefault if not controler else controler, name if controler else "default")(x())
            def __console(*args, **kwargs):
                # print(args, kwargs)
                return result(func)
            return __console
        return control

class OperationDefault(object):
    """默认的操作模块

    """
    @classmethod
    def default(cls, response):
    
        return response



        


def _parent_resoves():
    level_one = db.query("SELECT * FROM company_menu WHERE is_deleted=0 AND level=1")
    level_two = db.query("SELECT * FROM company_menu WHERE is_deleted=0 AND level=2")


    level_one_dict = {}
    for item in level_one:
        item["data"] = []
        level_one_dict[item["id"]] = item

    for item in level_two:
        if item["parent_id"] in level_one_dict.keys():
            
            level_one_dict[item["parent_id"]]["data"].append(item)

    return level_one_dict


def parse(regions):
    parent_2_children = {}
    data = []
    for item in regions:
        children = parent_2_children.get(item['parent_id'], [])
        children.append(item)
        parent_2_children[item['parent_id']] = children
    
    for root in parent_2_children[0]:
        data.append(build(root, parent_2_children))
    return data

def build(root, parent_2_children):
	node = {}
	node['id'] = root['id']
	node['name'] = root['name']
	if root['id'] in parent_2_children:
		node['list'] = []
		for item in parent_2_children[root['id']]:
			node['list'].append(build(item, parent_2_children))
	return node
