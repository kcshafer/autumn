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

    def get_object_fields(self, sobject):
        url = "%s/services/data/v29.0/sobjects/%s/describe" % (self.target, sobject)
        response = requests.get(url, headers=self.header)
        content = json.loads(response.content)

        return content.get('fields')

    def execute_anonymous(self, apex):
        url = "%s/services/data/v29.0/tooling/executeAnonymous" % (self.target)
        params = {'anonymousBody': apex}
        response = requests.get(url, headers=self.header, params=params)
        content = json.loads(response.content)

        return content

    def create(self, sobject, record, tooling=False):
        url = self.target + "/services/data/v29.0/"
        if tooling:
            url = url + 'tooling/sobjects/'
        else:
            url = url + 'sobjects/'
        url = url + sobject + '/'
        print url
        self.header['Content-Type'] = 'application/json'
        response = requests.post(url, headers=self.header, data=json.dumps(record))
        content = json.loads(response.content)

        return content

    def delete(self, sobject, id, tooling=False):
        url = self.target + "/services/data/v29.0/"
        if tooling:
            url = url + 'tooling/sobjects/'
        else:
            url = url + 'sobjects/'
        url = url + sobject + '/' + id
        print url
        response = requests.delete(url, headers=self.header)


    def query(self, query, tooling=False):
        url = self.target + "/services/data/v29.0/"
        if tooling:
            url = url + 'tooling/query/'
        else:
            url = url + 'query/'

        response = requests.get(url, headers=self.header, params={'q': query})
        content = json.loads(response.content)

        return content

    def debug_log(self, id):
        url = self.target + "/services/data/v29.0/tooling/sobjects/ApexLog/%s/Body" % id
        print url
        response = requests.get(url, headers=self.header)

        print response

        return response


    def run_tests(self, ids):
        id_str = ''
        print ids
        for id in ids:
            id_str = id_str + id + ','
        id_str = id_str.strip(',')
        print id_str

        url = self.target + "/services/data/v30.0/tooling/runTestsAsynchronous/?"
        response = requests.get(url, headers=self.header, params={'classids': id_str})

        content = json.loads(response.content)
        return content



