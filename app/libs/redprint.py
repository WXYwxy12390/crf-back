

class Redprint:

    def __init__(self,name):
        self.name = name
        self.mound = [] #先保存一系列的url,methods,fuction

    #这里的装饰器 仅仅是保存 url,methods,function到 mound中，通过register 统一绑定到蓝图
    def route(self,rule,**options):
        def decorator(f):
            self.mound.append((f,rule,options))
            return f
        return decorator

    def register(self,bp,url_prefix=None):
        if url_prefix == None:
            url_prefix = '/'+self.name
        #python 序列解包
        for f,rule,options in self.mound :
            #改变endpoint 使其加上模块名字  v1.module+view_function
            endpoint = self.name+'+'+options.pop("endpoint",f.__name__)
            #options 是字典,字典的pop方法是先查找有无这个key，
            # 然后删除(如果没有的话，取函数的名字为endpoint)
            bp.add_url_rule(url_prefix + rule,endpoint,f,**options)

