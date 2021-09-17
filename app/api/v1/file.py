import os

from flask import request, jsonify, current_app

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.utils.file import StaticFile
from app.utils.ocr import lab_inspectation_ocr

api = Redprint('file')


@api.route('/<string:folder>/<int:pid>/<int:id>')
def get_file(folder, pid, id):
    path = StaticFile(folder).get_file_info(id)
    data = {
        "code": 200,
        "data": path,
        "msg": "ok"
    }
    return jsonify(data)


@api.route('/<string:folder>/<int:pid>/<int:id>', methods=['POST'])
@auth.login_required
@edit_need_auth
def add_file(folder, pid, id):
    file = request.files['file']  # 获取到用户上传的文件对象file
    StaticFile(folder).add_file(id, file)
    path = os.path.join(current_app.static_folder, folder, str(id), file.filename)
    try:
        data = lab_inspectation_ocr(path, folder)
    except Exception as e:
        data = {}
    return Success(data=data)


@api.route('/<string:folder>/<int:pid>/<int:id>', methods=['DELETE'])
@auth.login_required
@edit_need_auth
def del_file(folder, pid, id):
    filename = request.get_json()['filename']
    static_file = StaticFile(folder)
    static_file.delete_file(id, filename)
    return Success()
