import shutil
import os
import sys
import re
import time

from flask import current_app

from app.libs.error_code import UploadFileError


class StaticFile():
    # static_folder = os.path.abspath('../krlz-back/app/static')
    # static_folder = os.getcwd() + '/app/static'

    def __init__(self,file_folder):
        self.static_folder = current_app.static_folder
        self.file_folder= self.static_folder + '/' + file_folder
        self.folder = file_folder

        print(self.file_folder)

    # 判断是否存在用户签名，如果有，返回签名路径
    def has_folder(self,id):
        path = os.path.join(self.file_folder, str(id))
        return os.path.exists(path)

    # 获取该文件夹下的一组文件信息
    def get_file_info(self,id):
        if not self.has_folder(id):
            return []
        path = os.path.join(self.file_folder, str(id))
        files = os.listdir(path)
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)  # 按照时间排序
        file_list = []
        for file in files:
            file_info = dict()
            file_info['id'] = id  # 查看文件的时候用
            size = os.path.getsize(os.path.join(path, file))
            file_info['file_size'] = "%.2f" % float(size / (1024 * 1024)) + "mb"  # 获取文件大小
            file_create_time = os.path.getctime(os.path.join(path, file))
            file_info['file_ctime'] = time.strftime("%Y-%m-%d", time.gmtime(file_create_time))  # 获取文件创建时间
            file_info['file_name'] = file
            file_info['file_path'] = os.path.join('/', self.folder, str(id), file)
            file_list.append(file_info)
        return file_list

    # 添加文件
    def add_file(self, id, file):
        # if self.has_file(id):  # 如果原来有签名，就删除
        #     clear_signature(user_id)

        filename = secure_filename(file.filename)
        suffix = os.path.splitext(filename)[1]  # 获取文件后缀名
        updir = self.file_folder + '/' + str(id)  # 拼接路径
        if suffix is not None:
            if not os.path.isdir(updir):  # 如果上传路径不存在
                os.makedirs(updir)
            if os.path.exists(os.path.join(updir, filename)):  # 如果需要上传的文件已经存在
                raise UploadFileError(msg='存在同名文件，上传失败')
            file.save(os.path.join(updir, filename))
            return True

    # 清理文件
    def clear_folder(self,id):
        path = os.path.join(self.file_folder, str(id))
        if os.path.exists(path):
            shutil.rmtree(path)  # 删除整个目录
            return True
        else:
            return False

    #删除文件
    def delete_file(self,id,filename):
        files = self.get_file_info(id)
        for file in files:
            if file['file_name'] == filename:
                os.remove(self.static_folder + file['file_path'])

    # file_list = []
    #
    # all_files = os.listdir(path)
    # all_files = sorted(all_files, key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)  # 按照时间排序
    #
    # for file in all_files:
    #     file_info = dict()
    #     file_info['id'] = evaluate_id  # 查看文件的时候用
    #     size = os.path.getsize(os.path.join(path, file))
    #     file_info['file_size'] = "%.2f" % float(size / (1024 * 1024)) + "mb"  # 获取文件大小
    #     file_create_time = os.path.getctime(os.path.join(path, file))
    #     file_info['file_ctime'] = time.strftime("%Y-%m-%d", time.gmtime(file_create_time))  # 获取文件创建时间
    #     file_info['file_name'] = file
    #     file_info['file_path'] = os.path.join('.', 'photo_evaluate', str(sample_id), str(cycle_number),
    #                                           str(evaluate_id), file)
    #     file_list.append(file_info)





PY2 = sys.version_info[0] == 2
text_type = str
_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = (
    "CON",
    "AUX",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
    "PRN",
    "NUL",
)


def secure_filename(filename):  # 重写这个方法，使它可以用于中文文件名

    if isinstance(filename, text_type):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('utf-8', 'ignore')  # 转码
        if not PY2:
            filename = filename.decode('utf-8')  # 解码
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')

    # myself define
    # 正则增加对汉字的过滤
    # \u4E00-\u9FBF 中文
    # 构建新正则

    _filename_ascii_add_strip_re = re.compile(r'[^A-Za-z0-9_\u4E00-\u9FBF.-]')

    # 使用正则
    filename = str(_filename_ascii_add_strip_re.sub('', '_'.join(filename.split()))).strip('._')

    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = "_" + filename

    return filename




