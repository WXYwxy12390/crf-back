from flask import request
from app.libs.error import Success
from app.libs.redprint import Redprint
from app.models.doubt import Doubt

api = Redprint('doubt')


@api.route('', methods=['POST'])
def get_doubts():
    data = request.get_json()
    doubt_ids = data.get('ids')
    doubt_ls = Doubt.query.filter(Doubt.is_delete == 0, Doubt.id.in_(doubt_ids)).all()
    return Success(data=doubt_ls if doubt_ls else {})
