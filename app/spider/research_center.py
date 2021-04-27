from app.libs.error_code import NotFound
from app.libs.httper import HTTP


class ResearchCenterSpider:
    project_url = 'http://127.0.0.1:40581/v1/research_centers?project_id={}'
    center_url = 'http://127.0.0.1:40581/v1/research_centers?research_center_id={}'
    user_center_url = 'http://127.0.0.1:40581/v1/research_centers?project_id={}&user_id={}'
    all_center_url = 'http://127.0.0.1:40581/v1/research_centers'
    def search_by_project(self, project_id):
        url = self.project_url.format(project_id)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到研究中心信息')
        return result

    def search_by_center(self, center_id):
        url = self.center_url.format(center_id)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到研究中心信息')
        return result

    def search_by_uid_project(self,project_id,center_id):
        url = self.user_center_url.format(project_id,center_id)
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到研究中心信息')
        return result

    def search_all(self):
        url = self.all_center_url
        result = HTTP.get(url)
        if result == {}:
            raise NotFound(msg='未找到研究中心信息')
        return result