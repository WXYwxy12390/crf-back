from app import create_app
from app.models.base import db
from app.models.base_line import Patient
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

    # patients = Patient.query.filter(Patient.is_delete == 0,
    #                                 Patient.researchCenter.in_([1, 12, 13, 14, 15, 16])).all()
    # for patient in patients:
    #     with db.auto_commit():
    #         account = patient.account[:]
    #         if not (54 in account):
    #             account.append(54)
    #         print(account, patient.account)
    #         patient.account = account
