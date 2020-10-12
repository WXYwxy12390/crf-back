
# class TestDict():
#     name = 'twc'
#     age = 18
#     def __init__(self):
#         self.sex = 'man'
#     def keys(self):
#         #注意返回一个元素的元组要在末尾加‘,’ 例如 ('name',)，否则会报错
#         #或者直接返回列表.
#         return ('name','age','sex') #元组/列表的序列
#
#     def __getitem__(self, item):
#         return getattr(self,item)
# o = TestDict()
#
# print(o.__dict__)
# print(dict(o))

strs = '[{"id": 0, "key": 0, "drugDose": "10g", "drugName": "啦啦啦", "duration": "9"},' \
       ' {"id": 1, "key": 1, "drugDose": "20g", "drugName": "啦啦", "duration": "24"}] '
strs = strs[1:-2]
print(strs)
strs = strs.replace('},','}*')
arr = strs.split('*')
print(arr)