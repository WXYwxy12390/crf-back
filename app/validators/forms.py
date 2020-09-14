# from wtforms import StringField, IntegerField
# from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
# from app.libs.enums import ClientTypeEnum
# from app.models.user import User
#
#
# from app.validators.base import BaseForm as Form #让表单验证继承我们自定义的验证器
# class ClientForm(Form):
#     account = StringField(validators=[DataRequired(message='不允许为空'),
#                                       length(min=5,max=32)])
#     # 可以没有密码
#     secret = StringField()
#
#     #客户端类型 ,取值要为客户端类型的几种，因此要自定义验证器
#     type = IntegerField(validators=[DataRequired()])
#
#
#     def validate_type(self,value):
#         try:
#             client = ClientTypeEnum(value.data) #通过 能否用枚举类型来进行类型转换 来验证
#         except ValueError as e:
#             raise  e
#         self.type.data = client  #这里必须将type的值赋值为枚举类型的
#
# #继承于ClientForm ,定制个性化验证
# class UserEmailForm(ClientForm):
#     account = StringField(validators=[
#         Email(message='invalidate email')
#     ])
#
#     secret = StringField(validators=[
#         DataRequired(),
#         Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}')
#     ])
#
#     nickname = StringField(validators=[DataRequired(),
#                                        length(min=2,max=22)])
#
#     #需要未被注册
#     def validate_account(self,value):
#        if User.query.filter_by(email=value.data).first():
#            raise ValidationError() #wtform 提供的异常,以后要自己处理
#
#
#
