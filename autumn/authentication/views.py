from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render
from django.http import HttpResponse

import json
import requests

def handle_callback(request):
    code = request.GET.get('code')
    redirect_uri = 'https://ec2-54-69-219-197.us-west-2.compute.amazonaws.com/callback'
    client_secret = '5669610576465531909'
    client_id = '3MVG9xOCXq4ID1uEEA_ToSIsz_uSYzfrt3vmYtibRmHQmm6xWh_fqEsiY542IoYRzpuYpIBCThY.8IwR5CgM.'
    resp = requests.post('https://login.salesforce.com/services/oauth2/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' % (code, client_id, client_secret, redirect_uri))
    content = json.loads(resp.content)

    request.session['access_token'] = content.get('access_token')

    return HttpResponse('success')

def check_id(request):
    return HttpResponse(request.session.get('access_token'))

