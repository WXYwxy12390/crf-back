from flask import request, jsonify

from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.utils.file import StaticFile

api = Redprint('file')


@api.route('/<string:folder>/<int:id>')
def get_file(folder,id):

    path = StaticFile(folder).get_file_info(id)
    data = {
        "code":200,
        "data":path,
        "msg":"ok"
    }
    return jsonify(data)


@api.route('/<string:folder>/<int:id>', methods=['POST'])
def add_file(folder, id):
    file = request.files['file']  # 获取到用户上传的文件对象file
    StaticFile(folder).add_file(id, file)
    return Success()


@api.route('/<string:folder>/<int:id>', methods=['DELETE'])
def del_file(folder, id):
    filename = request.get_json()['filename']
    static_file = StaticFile(folder)
    static_file.delete_file(id, filename)
    return Success()