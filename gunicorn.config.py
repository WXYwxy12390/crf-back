"""
@author: kid
@file: gunicorn.config.py
@time: 2020/1/12 14:34
"""
import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]
_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)

# 监听端口
bind = '0.0.0.0:85'

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 指定每个工作者的线程数
threads = 1

# 工作模式协程
worker_class = 'sync'

# 设置最大并发量
worker_connections = 2000

# 设置访问日志和错误信息日志路径
accesslog = '{}/logs/access.log'.format(path_of_current_dir)
errorlog = '{}/logs/error.log'.format(path_of_current_dir)

# 设置日志记录水平
loglevel = 'debug'
