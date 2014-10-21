import json
import requests

class Frisbee(object):

    def __init__(self, request):
        self.access_token = request.session.get('access_token')
        self.target = request.session.get('target')
        self.header = {'Authorization': 'Bearer %s' % self.access_token}

    def get_sobjects(self):
        url = self.target + '/services/data/v29.0/sobjects'
        response = requests.get(url, headers=self.header)
        content = json.loads(response.content)
        return content.get('sobjects')