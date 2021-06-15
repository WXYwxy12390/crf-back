from flask import current_app

from app.libs.error_code import NotFound
from app.libs.httper import HTTP
from app.config.common import RBAC_SCHEME, RBAC_IP, RBAC_PORT


class Project:
    url = '{}://{}:{}/v1/project/'.format(RBAC_SCHEME, RBAC_IP, RBAC_PORT) + '{}'

    def search_by_id(self, project_id):
        url = self.url.format(project_id)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到项目信息')
        return result

