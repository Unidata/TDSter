from xml.dom.minidom import parse
from helpers import basic_http_request

class TDSCatalog():

    def __init__(self, top_level_url):
        top_level_url = 'http://motherlode.ucar.edu:9080/thredds/catalog.xml'
        xml_data = basic_http_request(top_level_url, return_response = true)
        dom = parse(xml_data)

        for node in dom.getElementsByTagName('catalogRef'):
            print node.toxml()