

from flask_cors import CORS

from app.app import Flask


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    blueprint = create_blueprint_v1()
    app.register_blueprint(blueprint,url_prefix='/v1') #给蓝图 路由绑定固定的前缀/v1

def register_plugin(app):
    from app.models.base import db
    from app.models import base_line,crf_info,cycle,lab_inspectation,other_inspect,questionnaire,therapy_record

    db.init_app(app)
    with app.app_context():  #思考这段代码
        db.create_all()



def create_app():
    app = Flask(__name__)
    # 导入配置文件
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    CORS(app, resources={r"/*": {"origins": "*"}})
    register_blueprints(app)
    register_plugin(app)
    return app
