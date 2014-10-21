import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

from autumn.data.forms import QueryForm
from autumn.frisbee import Frisbee 

def query(request):
    frisbee = Frisbee(request)
    sobj_resp = frisbee.get_sobjects()

    sobjects = []
    for sobj in sobj_resp:
        if sobj.get('queryable'):
            sobjects.append(sobj.get('name'))

    return render(request, 'data/query_form.html', {'sobjects': sobjects})

def soql(request):
    access_token = request.session.get('access_token')
    header = {'Authorization': 'Bearer %s' % access_token}
    print request.POST
    params = {'q' : request.POST.get('query')}
    url = request.session.get('target') + '/services/data/v29.0/query'
    response = requests.get(url, headers=header, params=params)

    print response.content
    content = json.loads(response.content)
    records = content.get('records')
    fields = records[0].keys()
    #delete the unwanted attributes entry
    del fields[0]

    return render(request, 'data/query_results.html', {'fields': fields, 'records': records})

def fields(request):
    frisbee = Frisbee(request)
    response = frisbee.get_object_fields('Account')
    print response

    return HttpResponse(json.dumps(response))