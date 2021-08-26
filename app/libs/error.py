from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    # 基类api的默认值
    code = 200
    msg = 'sorry, we make a mistake'
    error_code = 999

    def __init__(self, msg=None, code=None,
                 error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        # 调用基类的构造函数
        # 第二个参数是传respone，不传falsk会自己构造一个
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        # request 的形式 类如 'POST v1/client/register'
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]

    # 获得不包含查询参数的路径
    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class Success(HTTPException):
    code = 200
    msg = 'ok'

    def __init__(self, msg=None, data=None, code=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data is not None:
            self.data = data
        # 调用基类的构造函数
        # 第二个参数是传respone，不传falsk会自己构造一个
        super(Success, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        # request 的形式 类如 'POST v1/client/register'
        body = dict(
            code=200,
            msg=self.msg
        )
        if hasattr(self, 'data'):
            body['data'] = self.data
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]
        # return [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", current_app.config['URL']),
        #         ("Access-Control-Allow-Methods", "*")]

    # 获得不包含查询参数的路径
    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
