import json
from lxml import etree

from autumn.frisbee import Frisbee

NS = {  
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/", 
        "urn": "urn:enterprise.soap.sforce.com"
    }

class SObject(object):

    def __init__(self, request, obj):
        frisbee = Frisbee(request)

        describe_xml = frisbee.describe_sobject(obj)
        describe_xml = etree.fromstring(describe_xml)
        xml_search_base = 'soapenv:Body/urn:describeSObjectResponse/urn:result/'
        self.activateable = describe_xml.xpath(xml_search_base + 'urn:activateable', namespaces=NS)[0].text
        self.key_prefix = describe_xml.xpath(xml_search_base + 'urn:keyPrefix', namespaces=NS)[0].text
        self.label = describe_xml.xpath(xml_search_base + 'urn:label', namespaces=NS)[0].text
        self.label_plural = describe_xml.xpath(xml_search_base + 'urn:labelPlural', namespaces=NS)[0].text
        self.layoutable = describe_xml.xpath(xml_search_base + 'urn:layoutable', namespaces=NS)[0].text
        self.mergeable = describe_xml.xpath(xml_search_base + 'urn:mergeable', namespaces=NS)[0].text
        self.name = describe_xml.xpath(xml_search_base + 'urn:name', namespace=NS)[0].text
        self.replicateable = describe_sobject.xpath(xml_search_base + 'urn:replicateable', namespaces)[0].text
        
    def to_json(self):
        return json.dumps(self.__dict__)