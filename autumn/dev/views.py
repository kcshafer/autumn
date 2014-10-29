from datetime import datetime, timedelta
import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

from autumn.frisbee import Frisbee 

def execute(request):
    return render(request, 'dev/execute_anonymous.html')

def execute_anonymous(request):
    frisbee = Frisbee(request)
    
    #### look for any existing TraceFlags and get rid of them if they exist ####
    query = "SELECT Id FROM TraceFlag WHERE TracedEntityId = '%s' Limit 1" % request.session.get('user_id')
    query_response = frisbee.query(query, tooling=True)
    try:
        if query_response:
            trace_id = query_response.get('records')[0].get('Id')
            frisbee.delete('TraceFlag', trace_id, tooling=True)
    except:
        print "query fail"

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
    #lines = log_response.content.split('\n')
    
    return HttpResponse(json.dumps(log_response.content))

def test_view(request):
    frisbee = Frisbee(request)
    query_response = frisbee.query('select symboltable from apexclass', tooling=True)
    test_classes = []
    for r in query_response.get('records'):
        if 'TEST' in r.get('SymbolTable').get('tableDeclaration').get('modifiers'):
            test_classes.append({'name': r.get('SymbolTable').get('name'), 'id': r.get('SymbolTable').get('key')})
        else:
            for m in r.get('SymbolTable').get('methods'):
                if 'TEST' in m.get('modifiers'):
                    test_classes.append(r.get('SymbolTable').get('name'))
                    break
    print test_classes
    return render(request, 'dev/run_tests.html', {'test_classes' : test_classes})

def run_tests(request):
    class_ids = request.POST.getlist('class_ids[]')
    frisbee = Frisbee(request)
    response = frisbee.run_tests(class_ids)
    print response
    return HttpResponse(response)

def retrieve_test_items(request):
    id = request.GET.get('id')
    query = "SELECT Id, Status, ApexClassId FROM ApexTestQueueItem WHERE ParentJobId = '%s'" % id
    frisbee = Frisbee(request)
    response = frisbee.query(query, tooling=True)
    print response

    return HttpResponse(json.dumps(response.get('records')))

def retrieve_test_results(request):
    id = request.GET.get('id')
    query = "SELECT ApexClassId, ApexLogId, Message, MethodName, Outcome, StackTrace FROM ApexTestResult WHERE AsyncApexJobId = '%s'" % id
    frisbee = Frisbee(request)
    response = frisbee.query(query, tooling=True)
    print response

    return HttpResponse(json.dumps(response.get('records')))

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