from app import create_app
from app.models.base import db
from app.models.base_line import Patient
from app.models.therapy_record import TreRec
from app.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.nickname = 'Super'
        user.password = '123456'
        user.email = '999@qq.com'
        user.auth = 2
        db.session.add(user)

    # all_treRec = TreRec.query.filter_by().all()
    # for treRec in all_treRec:
    #     with db.auto_commit():
    #         index = treRec.treNum
    #         treRec.treIndex = index