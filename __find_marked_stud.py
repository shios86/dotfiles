#!/Users/jye/.brew/bin/python3
import os
import requests as req
from getopt import gnu_getopt as getopt
from time import sleep
import sys

def _request(method:str, target:str,
             data:dict=None, headers:dict=None):
    prep = req.Request(method, target, data=data, headers=headers).prepare()
    # sign = hmac.new(secret, bytes(prep.body, 'utf-8'), digestmod=hashlib.sha256)
    # prep.body += '&signature=' + sign.hexdigest()
    # prep.url += '?' + prep.body
    with req.Session() as ses:
        ans = ses.send(prep)
    ans.raise_for_status()
    return ans

ENDPOINT = "https://api.intra.42.fr"
PATH = {
    'oauth': '/oauth/token',
    'location': '/v2/campus/{campus_id}/locations',
    'user_project': '/v2/users/{user_id}/projects_users',
    'project_user': '/v2/projects/{project_id}/projects_users',
    'p_slug_to_id': '/v2/projects/{project_id}'
}

TARGET = "{endpoint}{path}{param}"

CAMPUS = '1'

class PW42API:
    def __init__(self, public:str = None, secret:str = None):
        self._secret = secret
        self._public = public

        ans = _request(
            "POST",
            TARGET.format(endpoint=ENDPOINT, path=PATH['oauth'], param=''),
            data={
                'grant_type': 'client_credentials',
                'client_id': public,
                'client_secret': secret,
                'scope': 'projects public'
            }
        ).json()

        self.__token = ans['access_token']
        self.__expire = int(ans['created_at']) + int(ans['expires_in'])

    @property
    def secret(self):
        return self._secret

    @property
    def public(self):
        return self._public

    def has_done(self, user:str, proj_id:int):
        ans = _request(
            "GET",
            TARGET.format(
                endpoint=ENDPOINT,
                path=PATH['user_project'].format(user_id=user),
                param='?filter[marked]=true&filter[project_id]={0}'.format(proj_id),
            ),
            headers={'Authorization': 'Bearer {0}'.format(self.__token)}
        ).json()
        return ans

    def from_project_slug_to_id(self, project_slug:str):
        ans = _request(
            "GET",
            TARGET.format(
                endpoint=ENDPOINT,
                path=PATH['p_slug_to_id'].format(project_id=project_slug),
                param=''
            ),
            headers={'Authorization': 'Bearer {0}'.format(self.__token)}
        ).json()
        return int(ans['id'])

    def get_all_logged(self):
        res = []
        page = 1

        while True:
            ans = _request(
                "GET",
                TARGET.format(
                    endpoint=ENDPOINT,
                    path=PATH['location'].format(campus_id=CAMPUS),
                    param='?filter[active]=true&per_page=100&page={0}'.format(page)
                ),
                headers={'Authorization': 'Bearer {0}'.format(self.__token)}
            ).json()
            sleep(0.5)
            print(ans)
            if not ans:
                break
            res += ans
            page += 1

        return res

if __name__ == "__main__":
    opt, arg = getopt(sys.argv, '', ["secret=", "public=", "project="])

    secret = None
    public = None
    project = None

    for k, v in opt:
        if k == '--secret':
            secret = v
        elif k == '--public':
            public = v
        elif k == '--project':
            project = v

    if not secret or not public or not project:
        print("Please set your client public, secret and the project to look for")
        sys.exit(1)

    api = PW42API(public, secret)
    logged = api.get_all_logged()
    sleep(0.5)
    project_id = api.from_project_slug_to_id(project)

    for user in logged:
        sleep(0.5)
        p = api.has_done(user['user']['id'], project_id)
        if p:
            print(user['user']['id'], user['user']['login'], user['host'], True in (val['validated?'] for val in p[0]['teams']))
