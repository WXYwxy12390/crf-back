from flask import current_app

from app.config.secure import PROJECT_ID
from app.libs.error_code import NotFound
from app.libs.httper import HTTP
from app.config.common import RBAC_SCHEME, RBAC_IP, RBAC_PORT


class UserInfo:
    uid_url = '{}://{}:{}/v1/user'.format(RBAC_SCHEME, RBAC_IP, RBAC_PORT) + '?user_id={}'
    center_url = '{}://{}:{}/v1/user'.format(RBAC_SCHEME, RBAC_IP, RBAC_PORT) + '?research_center_id={}'
    roles_url = '{}://{}:{}/v1/user'.format(RBAC_SCHEME, RBAC_IP, RBAC_PORT) + '/by_roles/{}'.format(str(PROJECT_ID))

    def search_by_uid(self, uid):
        url = self.uid_url.format(uid)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到用户信息')
        return result

    def search_by_center(self, center_id):
        url = self.center_url.format(center_id)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到用户信息')
        return result

    @classmethod
    def search_by_role_ids(cls, role_ids):
        data = {'role_ids': role_ids}
        result = HTTP.post(cls.roles_url, data)
        if result == {}:
            raise NotFound(msg='未找到用户信息')
        return result
