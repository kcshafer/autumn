from datetime import datetime, timedelta
import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

from autumn.frisbee import Frisbee 

def execute_anonymous(request):
    frisbee = Frisbee(request)
    
    #### look for any existing TraceFlags and get rid of them if they exist ####
    query = "SELECT Id FROM TraceFlag WHERE TracedEntityId = '%s' Limit 1" % request.session.get('user_id')
    query_response = frisbee.query(query, tooling=True)
    if query_response.get('records'):
        trace_id = query_response.get('records')[0].get('Id')
        frisbee.delete('TraceFlag', trace_id, tooling=True)

    #### set trace flag ####
    TRACE_FLAG['ExpirationDate'] = (datetime.now() + timedelta(1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    TRACE_FLAG['TracedEntityId'] = request.session.get('user_id')
    TRACE_FLAG['ScopeId'] = request.session.get('user_id')
    traceflag_response = frisbee.create('TraceFlag', TRACE_FLAG, tooling=True)

    ####  execute apex ####    
    response = frisbee.execute_anonymous(request.POST.get('apex'))

    #### query for log ####
    query = "SELECT Id FROM ApexLog WHERE Request = 'API' AND LogUserId = '%s' ORDER BY StartTime desc" % request.session.get('user_id')
    query_response = frisbee.query(query, tooling=True)
    log_id = query_response.get('records')[0].get('Id')

    #### request log body ####
    log_response = frisbee.debug_log(log_id)
    lines = log_response.content.split('\n')
    
    return HttpResponse(json.dumps(lines))

def execute(request):
    return render(request, 'dev/execute_anonymous.html')


TRACE_FLAG = {
    'ApexCode': 'Debug',
    'ApexProfiling': 'Debug',
    'Callout': 'Debug',
    'Database': 'Debug',
    'System': 'Debug',
    'Validation': 'Debug',
    'Visualforce': 'Debug',
    'Workflow': 'Debug'
}