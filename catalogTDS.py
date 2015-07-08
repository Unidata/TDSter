import xml.etree.ElementTree as ET
from helpers import basic_http_request
from helpers.tdster_defaults import defaultTestCatalog
from string import join
import urllib2
import sys

class TDSCatalog():
    def __init__(self, catalogUrl):
        # top level server url
        self.catalogUrl = catalogUrl
        self.base_tds_url = catalogUrl.split('/thredds/')[0]
        if self.base_tds_url[-1] is not "/":
            self.base_tds_url = self.base_tds_url + "/"
        # get catalog.xml file
        xml_data = basic_http_request(catalogUrl, return_response = True)
        # begin parsing the xml doc
        tree = ET.parse(xml_data)
        root = tree.getroot()
        if root.attrib.has_key("name"):
            self.catalog_name = root.attrib["name"]
        else:
            self.catalog_name = "No name found"

        self.datasets = {}
        self.services = []
        self.catalogRefs = {}
        for child in root.iter():
            tagType = child.tag.split('}')[-1]

            if tagType == "service":
                if child.attrib["serviceType"] != "Compound":
                    self.services.append(SimpleService(child))
            elif tagType == "dataset":
                if child.attrib.has_key("urlPath"):
                    if child.attrib["urlPath"].endswith("latest.xml"):
                        ds = Dataset(child, catalogUrl)
                    else:
                        ds = Dataset(child)
                    self.datasets[ds.name] = ds
            elif tagType == "catalogRef":
                catalogRef = CatalogRef(child)
                self.catalogRefs[catalogRef.title] = catalogRef

        self.numberOfDatasets = len(self.datasets.keys())
        for dsName in self.datasets.keys():
            self.datasets[dsName].makeAccessUrls(self.base_tds_url, self.services)

class CatalogRef():
    def __init__(self, elementNode):
        self.name = elementNode.attrib["name"]
        self.href = elementNode.attrib["{http://www.w3.org/1999/xlink}href"]
        if self.href[0] == '/':
            self.href = self.href[1:]
        self.title = elementNode.attrib["{http://www.w3.org/1999/xlink}title"]

class Dataset():
    def __init__(self, elementNode, catalogUrl = ""):
        self.name = elementNode.attrib['name']
        self.urlPath = elementNode.attrib['urlPath']
        self.resolved = False
        self.resolverUrl = None
        # if latest.xml, resolve the latest url
        if self.urlPath.endswith("latest.xml"):
            if catalogUrl != "":
                self.resolved = True
                self.resolverUrl = self.urlPath
                try:
                    self.urlPath = self.resolveUrl(catalogUrl)
                except ET.ParseError:
                    print self.name
                    print self.urlPath
                    self.resolved = False
                    pass
            else:
                print "Must pass along the catalog URL to resolve the latest.xml dataset!"

    def resolveUrl(self,catalogUrl):
            if catalogUrl != "":
                resolverBase = catalogUrl.split("catalog.xml")[0]
                resolverUrl = resolverBase + self.urlPath
                resolverXml = basic_http_request(resolverUrl, return_response = True)
                tree = ET.parse(resolverXml)
                root = tree.getroot()

                self.catalog_name = root.attrib["name"]
                found = False
                for child in root.iter():
                    if not found:
                        tagType = child.tag.split('}')[-1]
                        if tagType == "dataset":
                            if child.attrib.has_key("urlPath"):
                                ds = Dataset(child)
                                resolvedUrl = ds.urlPath
                                found = True
                if found:
                    return resolvedUrl
                else:
                    print "no dataset url path found in latest.xml!"

    def makeAccessUrls(self, catalogUrl, services):
        accessUrls = {}
        serverUrl = catalogUrl.split('/thredds/')[0]
        for service in services:
            if service.serviceType != 'Resolver':
                accessUrls[service.serviceType] = serverUrl + service.base + self.urlPath

        self.accessUrls = accessUrls


class SimpleService():
    def __init__(self, serviceNode):
        self.name = serviceNode.attrib['name']
        self.serviceType = serviceNode.attrib['serviceType']
        self.base = serviceNode.attrib['base']

class CompoundService():
    def __init__(self, serviceNode):
        self.name = serviceNode.attrib['name']
        self.serviceType = serviceNode.attrib['serviceType']
        self.base = serviceNode.attrib['base']
        services = []
        for child in list(serviceNode):
          services.append(SimpleService(child))

        self.services = services

def fullCatalogInv(url):
        cat = TDSCatalog(url)
        names = cat.datasets.keys()
        names.sort()

        refs = cat.catalogRefs.keys()
        refs.sort()

        print("Datasets:")
        for name in names:
            print("    {}".format(name,))

        if refs != []:
            print("CatalogRefs:")
            for ref in refs:
                print("    {}".format(ref,))

        if refs != []:
            for ref in refs:
                fullCatalogInv(join([cat.base_tds_url,cat.catalogRefs[ref].href],'/'))

def applyTestFullCatalogInv(url, testFunc = None, datasetKey="latest"):
      success = False
      def defaultTestFunc(x):
          print x.name
          #for key in x:
          #    print(key)

      if testFunc is None:
          testFunc = defaultTestFunc

      if "FNMOC" not in url:
        try:
            cat = TDSCatalog(url)
            success = True
        except urllib2.HTTPError, e:
            print(e.code, e.reason, url)
            success = False
            pass

        if success:
            names = cat.datasets.keys()
            names.sort()

            refs = cat.catalogRefs.keys()
            refs.sort()
            for name in names:
                testUrl = cat.datasets[name].urlPath
                if cat.datasets[name].resolved:
                    testUrl = cat.datasets[name].resolverUrl

                if datasetKey in testUrl:
                    try:
                        testFunc(cat.datasets[name])
                    except ET.ParseError:
                        pass

            if refs != []:
                for ref in refs:
                    tmpRef = cat.catalogRefs[ref].href
                    if tmpRef[0] == "/":
                        tmpRef = tmpRef[1:]

                    applyTestFullCatalogInv(cat.base_tds_url + tmpRef,
                                            testFunc=testFunc, datasetKey=datasetKey)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Find all datasets on TDS server")
    parser.add_argument("-u", "--url", default=defaultTestCatalog,
        help="url of the TDS catalog xml file you wish to begin crawling")
    args = parser.parse_args()

    url = args.url
    #fullCatalogInv(server)
    applyTestFullCatalogInv(url)
