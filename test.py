import numpy as np
from time import time
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

# strs = '[{"id": 0, "key": 0, "drugDose": "10g", "drugName": "啦啦啦", "duration": "9"},' \
#        ' {"id": 1, "key": 1, "drugDose": "20g", "drugName": "啦啦", "duration": "24"}] '
# strs = strs[1:-2]
# print(strs)
# strs = strs.replace('},','}*')
# arr = strs.split('*')
# print(arr)

# a = []
# b = np.zeros(0,dtype=str)
# time1 = time()
# for i in range(0, 10000):
#     a.append('/')
# time2 = time()
# for i in range(0, 10000):
#     b = np.append(b, '/')
# time3 = time()
# print('append操作')
# print('使用列表：' + str(time2-time1))
# print('使用numpy：' + str(time3-time2))
# a = []
# b = np.zeros(0,dtype=str)
# time1 = time()
# for i in range(0, 1000):
#     a.extend(['/']*1000)
# time2 = time()
# for i in range(0, 1000):
#     b = np.append(b, np.array(['/']*1000))
# time3 = time()
# print('extend操作')
# print('使用列表：' + str(time2-time1))
# print('使用numpy：' + str(time3-time2))

time1 = time()
a = ['/']*1000
for i in range(0,100):
    a.extend(['/']*100)
print(time()-time1)

time2 = time()
b = np.array(['/']*10)
for i in range(0,100):
    b = np.append(b, ['/']*100)
print(time()-time2)