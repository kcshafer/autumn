from django.shortcuts import render
from django.http import HttpResponse

import json
from lxml import etree
import xlsxwriter

from autumn.frisbee import Frisbee
from autumn.org.sobject import SObject

NS = {  
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/", 
        "urn": "urn:enterprise.soap.sforce.com"
    }

OVERVIEW = {
    'name'        : 'Name',
    'label'       : 'Label',
    'labelPlural' : 'Label Plural',
    'keyPrefix'   : 'Key Prefix',
    'createable'  : 'Creatable',
    'custom'      : 'Custom',
    'deleteable'  : 'Deleteable',
    'feedEnabled' : 'Feed Enabled',
}

FIELDS = {
    'custom'         : 'Custom',
    'length'         : 'Length',
    'name'           : 'Name',
    'nillable'       : 'Nillable',
    'permissionable' : 'Permissionable',
    'sortable'       : 'Sortable',
    'type'           : 'Type',
    'unique'         : 'Unique',
    'updateable'     : 'Updateable',
}

ALPHA = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
]

def sobject_overview(request):
    frisbee = Frisbee(request)
    sobj_resp = frisbee.get_sobjects()

    sobjects = []
    for sobj in sobj_resp:
        if sobj.get('queryable'):
            sobjects.append(sobj.get('name'))
            
    return render(request, 'org/sobject_overview.html', {'sobjects': sobjects})

def generate_sobject(request):
    sobject_name = request.GET.get('sobject')
    frisbee = Frisbee(request)

    describe_xml = frisbee.describe_sobject(sobject_name)
    describe_xml = etree.fromstring(describe_xml)

    sobject = {}
    for el in  describe_xml.xpath('soapenv:Body/urn:describeSObjectResponse/urn:result', namespaces=NS)[0].iterchildren():
        if not el.getchildren():
            sobject[el.tag.replace('{'+NS.get('urn')+'}', '')] = el.text

    fields = []
    for el in describe_xml.xpath('soapenv:Body/urn:describeSObjectResponse/urn:result/urn:fields', namespaces=NS):
        field = {}
        for attr in el.iterchildren():
            field[attr.tag.replace('{'+NS.get('urn')+'}', '')] = attr.text

        fields.append(field)

    sobject['fields'] = fields

    child_relationships = []
    for el in describe_xml.xpath('soapenv:Body/urn:describeSObjectResponse/urn:result/urn:childRelationships', namespaces=NS):
        child_relationship = {}
        for attr in el.iterchildren():
            child_relationship[attr.tag.replace('{'+NS.get('urn')+'}', '')] = attr.text

        child_relationships.append(child_relationship)

    sobject['child_relationships'] = child_relationships

    vr_results = frisbee.query('SELECT Id, Metadata, ValidationName FROM ValidationRule', tooling=True)
    sobject['validation_rules'] = vr_results.get('records')

    return HttpResponse(json.dumps(sobject))

def generate_excel(request):
    sobject = json.loads(request.POST.get('raw_sobject'))
    workbook = xlsxwriter.Workbook('demo.xls')
    overview_sheet = workbook.add_worksheet('Overview')
    
    if request.POST.get('overview') == 'on':
        x = 1
        for k, v in OVERVIEW.iteritems():
            overview_sheet.write('A%s' % x, v)
            overview_sheet.write('B%s' % x, sobject.get(k))
            x=x+1

    fields_sheet = workbook.add_worksheet('Fields')
    if request.POST.get('fields') == 'on':
        y = 0
        x = 2
        for k, v in FIELDS.iteritems():
            fields_sheet.write('%s1' % ALPHA[y], v)
            y=y+1

        for field in sobject.get('fields'):
            y=0
            for k, v in FIELDS.iteritems():
                fields_sheet.write('%s%s' % (ALPHA[y], x), field.get(k))
                y=y+1
            x=x+1

    workbook.close()
    
    f = open('demo.xls', 'r')

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="test.xls"'
    response.write(f.read())
    
    return response
