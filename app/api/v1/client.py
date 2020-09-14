# from flask import request
#
# from app.libs.enums import ClientTypeEnum
# from app.libs.error_code import ClientTypeError, Success
# from app.libs.redprint import Redprint
# from app.models.user import User
# from app.validators.forms import ClientForm, UserEmailForm
#
# api = Redprint('client')
#
# #注册  登录的api 最好做成统一的接口
#
# @api.route('/register',methods=['POST'])
# def create_client():
#
#     #表单 网页
#     #json 移动端
#
#     form = ClientForm().validate_for_api()  #如果是对json格式验证,要用data= ，看看源码才知道
#     # if form.validate():
#     #     #根据type种类来注册用户
#     #     promise = {
#     #         ClientTypeEnum.USER_EMAIL:__register_user_by_email
#     #     }
#     #
#     #     promise[form.type.data]()
#     # else:
#     #     raise ClientTypeError #抛出自定义类型错误
#     promise = {
#         ClientTypeEnum.USER_EMAIL: __register_user_by_email
#     }
#     promise[form.type.data]()
#     return Success()
#
# def __register_user_by_email():
#     #nickname如何拿到？ 验证器中没有相关字段 原则上我们需要从 form中拿到数据，这些数据是通过验证的
#     # request.json['nickname']
#     form = UserEmailForm().validate_for_api()
#     User.register_by_email(form.nickname.data,
#                            form.account.data,
#                            form.secret.data)
