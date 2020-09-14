#重写WTForms,使得它可以抛出错误异常
from flask import request
from wtforms import  Form

from app.libs.error_code import ParameterException


class BaseForm(Form):
    #data 是因为我们在client中需要一个data的json数据
    def __init__(self):
        data = request.json #这句代码，直接不用我们在外部传入数据了，直接获取
        super(BaseForm,self).__init__(data=data)

    def validate(self):
        pass
    #可以自定义validate ,也可以覆盖原有的validate
    def validate_for_api(self):
        valid = super(BaseForm,self).validate()
        if not valid :
            # 把错误传到我们自定义的参数错误码中
            raise ParameterException(msg=self.errors)
        return self #self就是form对象