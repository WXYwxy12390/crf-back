from app.models.base_line import Patient


def sort_samples_while_query(after_filter, way):
    if way == 1:
        # 按患者编号倒序
        return after_filter.order_by(Patient.patNumber.desc()).all()
    elif way == 2:
        # 按患者编号正序
        return after_filter.order_by(Patient.patNumber.asc()).all()
    elif way == 3:
        # 按创建时间倒序排列
        return after_filter.order_by(Patient.create_time.desc()).all()
    elif way == 4:
        # 按创建时间正序排列
        return after_filter.order_by(Patient.create_time.asc()).all()
    elif way == 5:
        # 按更新时间正序排列
        return after_filter.order_by(Patient.update_time.asc()).all()
    else:
        # 按更新时间倒叙排列
        return after_filter.order_by(Patient.update_time.desc()).all()
