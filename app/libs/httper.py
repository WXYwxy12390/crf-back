import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url, headers={'Connection': 'close'})
        # restful
        # json
        """
                if r.status_code == 200 :
                    if return_json:
                        return r.json()
                    else:
                        return r.text
                else :
                    if return_json :
                        return {}
                    else:
                        return ''
        """
        if r.status_code != 200 or r.json()['code'] != 200:
            return {} if return_json else r.text
        else:
            return r.json() if return_json else r.text
