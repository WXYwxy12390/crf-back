from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import  HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPTokenAuth()
User = namedtuple('User',['user_id','scopes'])

# 权限控制
@auth.verify_token
def verify_token(token):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info  # 存入当前user信息进flask g变量,方便后续api相关操作
        allow = is_in_scope(g.user.scopes, request.endpoint)
        if not allow:
            raise Forbidden()
        return True


# 核对当前token的合法性且未过期
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    # 如果无法解密,当前token无效
    # 根据不同错误信息,返回具体的错误信息
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=10031)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=10032)
    user_id = data['user_id']
    scopes = data['scopes']
    # user_name = data['user_name']
    # request 视图函数
    return User(user_id, scopes)