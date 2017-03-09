


def register(cls, *args, **kwarg):

    print(cls, args, kwarg, 'one')
    def detor(*args, **kw):
        
        print(args, kw, 'two')
    
    return detor



class ooop(object):

    def __init__(self):
        register('123', '2345','2321', l = '2345')(self.fn)

    def fn(self):
        pass
        


class ValStats(object):
    
    @classmethod
    def func(self, *args, **kwarg):
        print(args)

    @classmethod
    def execute(cls):
        
        cls.func(456,789)




def output(number):
    print('()' * number)

def print_paren(result, left, right):
    if left == 0 and right == 0:
        print(result)
    elif left == 0 and right > 0:
        print_paren(result+")", left, right-1)
    else:
        if left == right:
            print_paren(result+"(", left-1, right)
        elif left < right:
            print_paren(result+"(", left-1, right)
            print_paren(result+")", left, right-1)

if __name__ == '__main__':
    
    # print_paren('', 2, 2)

    ValStats.execute()
