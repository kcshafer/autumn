from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import json
import requests

def authentication_landing(request):
    prod_url = "https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9xOCXq4ID1uEEA_ToSIsz_uSYzfrt3vmYtibRmHQmm6xWh_fqEsiY542IoYRzpuYpIBCThY.8IwR5CgM.&redirect_uri=https%3A%2F%2Fec2-54-69-219-197.us-west-2.compute.amazonaws.com%2Fcallback&state=mystate"
    sandbox_url = "https://test.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9xOCXq4ID1uEEA_ToSIsz_uSYzfrt3vmYtibRmHQmm6xWh_fqEsiY542IoYRzpuYpIBCThY.8IwR5CgM.&redirect_uri=https%3A%2F%2Fec2-54-69-219-197.us-west-2.compute.amazonaws.com%2Fcallback&state=mystate"
    
    return render(request, 'authentication/landing.html', {'prod_url': prod_url, 'sandbox_url': sandbox_url})


def handle_callback(request):
    code = request.GET.get('code')

    redirect_uri = 'https://ec2-54-69-219-197.us-west-2.compute.amazonaws.com/callback'
    client_secret = '5669610576465531909'
    client_id = '3MVG9xOCXq4ID1uEEA_ToSIsz_uSYzfrt3vmYtibRmHQmm6xWh_fqEsiY542IoYRzpuYpIBCThY.8IwR5CgM.'
    resp = requests.post('https://login.salesforce.com/services/oauth2/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' % (code, client_id, client_secret, redirect_uri))
    content = json.loads(resp.content)

    #id service 
    id_response = requests.get(content.get('id'), headers={'Authorization': 'Bearer %s' % content.get('access_token')})
    user = json.loads(id_response.content)

    request.session['name'] = user.get('display_name')
    request.session['email'] = user.get('email')
    request.session['username'] = user.get('username')
    request.session['user_id'] = user.get('user_id')
    request.session['access_token'] = content.get('access_token')
    request.session['target'] = content.get('instance_url')
    request.session['org_id'] = user.get('organization_id')

    return HttpResponseRedirect('/data/query')

#clears session data with salesforce access token
def logout(request):
    del request.session['access_token']
    del request.session['target']

    return HttpResponseRedirect('/login')

