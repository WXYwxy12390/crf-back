# 将json所有字段插入到对应表的对应字段中
from app.models.base import db


def json2db(jsondata, table):
    # if jsondata['sample_id'] is not None:
    #     sample = Sample.query.get_or_404(jsondata['sample_id'])
    #     if sample.is_submit == 1:
    #         return
    with db.auto_commit():
        new_record = table()
        for k in jsondata:
            # print(k, jsondata[k])
            if jsondata is not None:
                setattr(new_record, k, jsondata[k])
        db.session.merge(new_record)
        # db.session.commit()


def json2db_add(jsondata, table):
    new_record = table()
    for k in jsondata:
        # print(k, jsondata[k])
        if jsondata is not None:
            setattr(new_record, k, jsondata[k])
    db.session.add(new_record)
    db.session.flush()
    db.session.commit()
    return new_record

def delete_array(model_items):
    with db.auto_commit():
        for item in model_items:
            item.delete()