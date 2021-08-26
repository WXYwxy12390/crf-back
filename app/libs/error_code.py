from app.libs.error import APIException


# class Success(APIException):
#     code = 201 #新增成功
#     msg = 'ok'
#     error_code = 0
#
# class DeleteSuccess(Success):
#     code = 202 #删除成功
#     error_code = 1
class ServerError(APIException):
    # code = 500
    msg = 'sorry, we made a mistake ^_^'
    error_code = 999


# class ClientTypeError(APIException):
#     # 原HTTPException 会返回html,我们需要json格式的
#     # 我们自定义一个APIExcetion ,然后让其继承
#     code = 400
#     msg = 'client is invalid'
#     error_code = 1006

# 为我们自定义的validator验证器,定制错误码

class ParameterException(APIException):
    # code = 400
    msg = 'invalid parameter'
    error_code = 1001


class NotFound(APIException):
    # code = 404

    msg = 'the resource are not found O__O...'
    error_code = 1002


class AuthFailed(APIException):
    # code = 401
    error_code = 1003
    msg = 'authorization failed'


class Forbidden(APIException):
    # code = 403
    error_code = 1004
    msg = '权限不足'


class GetFileError(APIException):
    # code = 404
    msg = 'the File are not found O__O...'
    error_code = 1005


class UploadFileError(APIException):
    # code = 405
    msg = 'upload the File failed'
    error_code = 1006


class SignatureIsExist(APIException):
    msg = '当前用户已经存在签名'
    error_code = 10010


class SignatureNotFound(APIException):
    msg = '当前用户还没有签名'
    error_code = 1011


class NotCurrentUser(Forbidden):
    error_code = 2001
    msg = '该样本非本用户所创建'


class SubmitError(Forbidden):
    # code = 403
    error_code = 1007
    msg = '已提交,无法进行修改'


class SampleStatusError(Forbidden):
    # code = 403
    error_code = 1008
    msg = '样本状态有误'


class SignatureError(Forbidden):
    # code = 403
    error_code = 10011
    msg = '已经存在签名'


class NoProjectId(Forbidden):
    # code = 403
    error_code = 10041
    msg = '无法获取项目id'


class PostError(Forbidden):
    error_code = 10021
    msg = 'Post Error!'
