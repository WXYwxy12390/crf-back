# from flask import jsonify, g
#
# from app.libs.error_code import DeleteSuccess
# from app.libs.redprint import Redprint
# from app.libs.token_auth import auth
# from app.models.base import db
# from app.models.user import User
#
# api = Redprint('user')
#
# @api.route('/<int:uid>',methods=['GET'])
# @auth.login_required
# def super_get_user(uid):
#     user = User.query.filter_by(id=uid).first_or_404()
#     #不能直接返回user 模型
#     #思路一:将user的数据保存在字典中，然后返回json格式的
#     #思路二: 1.重写jsonify 中的default方法，使得返回 dict(对象)
#     #        2. 在user 模型下添加方法，keys，__getitem__ ,指定我们应序列化的属性
#     return jsonify(user)
#
# @api.route('',methods=['GET'])
# @auth.login_required
# def get_user():
#     uid = g.user.uid #g变量读取id防止超权
#     user = User.query.filter_by(id=uid).first_or_404()
#     return jsonify(user)
#
#
#
# #管理员
# @api.route('/<int:uid>',methods=['DELETE'])
# def super_delete_user(uid):
#     pass
#
# @api.route('',methods=['DELETE'])
# @auth.login_required
# def delete_user():
#     #g变量是线程隔离的
#     uid = g.user.uid  #用namedTuple 的好处，此时我们可以用对象.属性 的形式来获得数据
#     with db.auto_commit():
#         user = User.query.filter_by(id=uid).first_or_404()
#         user.delete()
#
#     return  DeleteSuccess()