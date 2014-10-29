import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

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
    print request.GET
    query = request.GET.get('query')
    frisbee = Frisbee(request)
    response = frisbee.query(query)
    print response
    records = response.get('records')

    return HttpResponse(json.dumps(records))

def fields(request):
    frisbee = Frisbee(request)
    response = frisbee.get_object_fields(request.GET.get('sobject'))

    return HttpResponse(json.dumps(response))
