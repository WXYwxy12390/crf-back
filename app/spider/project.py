from flask import current_app

from app.libs.error_code import NotFound
from app.libs.httper import HTTP


class Project:
    url = 'http://127.0.0.1:81/v1/project/{}'

    def search_by_id(self, project_id):
        url = self.url.format(project_id)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到项目信息')
        return result

