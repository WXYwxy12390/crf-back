
class TestDict():
    name = 'twc'
    age = 18
    def __init__(self):
        self.sex = 'man'
    def keys(self):
        #注意返回一个元素的元组要在末尾加‘,’ 例如 ('name',)，否则会报错
        #或者直接返回列表.
        return ('name','age','sex') #元组/列表的序列

    def __getitem__(self, item):
        return getattr(self,item)
o = TestDict()

print(o.__dict__)
print(dict(o))


