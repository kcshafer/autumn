from datetime import datetime, timedelta
import json
from lxml import etree
import requests

from django.shortcuts import render
from django.http import HttpResponse

from autumn.frisbee import Frisbee, META_NS, META_NS_RESPONSE

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

def retrieve_metadata(request):
    metadata = {}
    frisbee = Frisbee(request)
    cls_response = frisbee.query('SELECT Id, Name FROM ApexClass')
    object_response = frisbee.query('SELECT DeveloperName FROM CustomObject')
    metadata['classes'] = cls_response.get('records')
    all_sobjects = frisbee.get_sobjects()
    sobjects = []
    for sobj in all_sobjects:
        if sobj.get('retrieveable') == True:
            sobjects.append(sobj.get('name'))

    metadata['sobjects'] = sobjects

    return render(request, 'dev/retrieve_metadata.html', metadata)

def download_metadata(request):
    print "POST VALUES"
    print request.POST
    package = etree.parse('autumn/frisbee/soap/package.xml')
    package = package.getroot()
    for mt in METADATA_TYPES:
        pkg_member = etree.Element('types')
        name = etree.Element('name')
        name.text = mt
        pkg_member.append(name)
        for member in request.POST.getlist(mt):
            print member
            members = etree.Element('members')
            members.text = member
            pkg_member.append(members)
        package.xpath('soapenv:Body/ns1:retrieve/ns1:RetrieveRequest/ns2:unpackaged', namespaces=META_NS)[0].append(pkg_member)

    frisbee = Frisbee(request)
    async_id = frisbee.retrieve_request(package)
    status_xml = None
    while True:
        status_xml = frisbee.check_retrieve_status(async_id)
        print "=====================STATUS=========================="
        print status_xml.xpath('soapenv:Body/xmlns:checkRetrieveStatusResponse/xmlns:result/xmlns:done', namespaces=META_NS_RESPONSE)[0].text
        if status_xml.xpath('soapenv:Body/xmlns:checkRetrieveStatusResponse/xmlns:result/xmlns:done', namespaces=META_NS_RESPONSE)[0].text == 'true':
            break
    print "================ZIP FILE============================="
    zip_binary = status_xml.xpath('soapenv:Body/xmlns:checkRetrieveStatusResponse/xmlns:result/xmlns:zipFile', namespaces=META_NS_RESPONSE)[0].text
    frisbee.binary_to_zip(zip_binary)
    
    f = open('%s.zip' % (request.session.get('user_id')), 'r')

    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename="retrieve.zip"'
    response.write(f.read())
    
    return response


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

METADATA_TYPES = [
    'ApexClass',
    'CustomObject',
]