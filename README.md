# 项目结构

**api层**

1. 该层定义了所有 后端api接口

2. API的版本号放入URL，例如 https://api.example.com/v1/

**config**

该层定义了项目相关的配置信息，例如jwt加密的SECRET_KEY，数据库的连接地址

```python
class TestConfig(Config):
    DEBUG = True
    # SERVER_NAME = '{}:{}'.format('0.0.0.0', 5000)
    # local docker mysql
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMT_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    TOKEN_EXPIRATION = 24 * 3600 * 100

    LOGGING_LEVEL = logging.INFO

config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
```

**libs**

**error.py**

原生的flask框架提供的api异常提示是html形式的，不易前端使用，因此定义了API异常类，将后端中的api异常以JSON的格式呈现给前端。

```python
class APIException(HTTPException):
    # code = 500
    code = 200
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", "*"),
                ("Access-Control-Allow-Methods", "*")]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
```



**token_auth.py**

该层主要是配合@auth.login_required注解，对api进行访问权限控制

```python
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
```

**models**

该层主要是定义了数据库模型对象，本项目才有的是flask-sqlalchemy，orm是应用面向对象思想，将数据库记录映射为模型对象。

为了保证数据库的安全性，不应使用orm来生成数据库表和字段的修改，而是应该先在数据库中进行更改，再修改orm模型类。



# 规范说明

**统一返回格式**

服务器返回的数据格式，应该尽量使用JSON，避免使用XML。

***请求数据成功应注意的点***

1. 若查询出的数据是空对象，应直接返回null
2. 若查询出的数据是空数组，应直接返回空数组，

```
{
    "code": 200,
    "data": [],
    "message": "ok",
}

```

***请求失败应注意的点***

应提供异常接口的相关信息，例如错误码，错误消息，接口路由等。

```
{
    "error_code": 10003,
    "message": "ok",
    "request":"url/path"
}
```



**统一异常处理**

利用AOP思想和flask提供的全局异常处理器，进行统一的异常处理

```python
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
```

对项目中可能的异常进行分类，并对前端提供错误码列表

```python
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
```





# Install

## 一、 安装必备软件
```bash
pip3 install pipenv
pipenv install --ignore-pipfile
```
## 二、相关代码操作

**更新代码**

```bash
git clone https://git.dev.tencent.com/kid_1412/pet-flask.git
cd pet-flask
# 上面两行只在第一次拉取代码仓库时需要
git pull
```



**修改相关代码**

- 修改`rwe.py`中`app=create_app('dev')`为`app=create_app('prod')`
- 修改`app/config/setting.py`中`ProdConfig`类，`SQLALCHEMY_DATABASE_URI`对应的`db_`开头的几项数据库配置
- 修改 ‘app/config/setting.py’中 ’Config‘ 类 ，‘RBAC_URL’ 对应的ip和端口
- 修改`gunicorn.config.py`中`bind=`一行的端口号

**运行程序**

```bash
pipenv run gunicorn -D wsgi -c gunicorn.config.py
```

以后更新代码时，要关闭之前运行的进程，再更新代码

```
pstree -ap|grep gunicorn  查看运行的后台gunocorn进程
kill -9 进程号
git pull
pipenv run gunicorn -D wsgi -c gunicorn.config.py
```



