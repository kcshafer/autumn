import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

from autumn.data.forms import QueryForm

def query(request):
    query_form = QueryForm()

    return render(request, 'data/query_form.html', {'query_form': query_form})

def soql(request):
    access_token = request.session.get('access_token')
    header = {'Authorization': 'Bearer %s' % access_token}
    params = {'q' : request.POST.get('query')}
    #url = request.session.get('target') + '/services/data/v20.0/query'
    url = 'https://na17.salesforce.com/services/data/v20.0/query'
    response = requests.post(url, headers=header, params=params)

    print response.content
    records = json.loads(response.content)

    return HttpResponse('success')