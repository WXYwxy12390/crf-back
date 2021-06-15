from flask_sqlalchemy import get_debug_queries
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config['FLASKY_DB_QUERY_TIMEOUT']:
            # query.statement：查询的sql
            # query.duration： 耗时
            # 打印超时sql和时间
            print('----慢sql-----\t\nsql:\t\n {sql} \n\t耗时:{duration}'.format(sql=query.statement,
                                                                             duration=query.duration))
    return response


# 利用AOP思想统一处理异常
# flask提供的处理全局异常
@app.errorhandler(Exception)
def framework_error(e):
    # APIException
    # HTTPException
    # Exception

    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            # 在开发模式下，我们还是返回具体的堆栈错误信息
            raise e


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=40585,ssl_context=('server.pem','server.key'))
    
