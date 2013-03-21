from xml.dom import minidom as md
from helpers import basic_http_request
from helpers.tdster_defaults import testServer
from string import join

class TDSCatalog():
    def __init__(self, top_level_url):
        self.base_tds_url = top_level_url.split('/thredds/')[0]
        xml_data = basic_http_request(top_level_url, return_response = True)
        doc = md.parse(xml_data)
        root = doc.firstChild
        all_nodes = [e for e in root.childNodes if e.nodeType == e.ELEMENT_NODE]
        self.nodes = self.node_to_dict(all_nodes)
        # find nested catalogs
        self.nested_catalogs = root.getElementsByTagName('catalogRef')
        datasets = []
        for e in root.childNodes:
            if ((e.nodeType == e.ELEMENT_NODE) and (e.nodeName == 'dataset')):
                datasets.append(TDSdataset(root, e))

        self.datasets = datasets

    def node_to_dict(self, all_nodes):
        nodes = {}
        for node in all_nodes:
            node_name = node.nodeName
            if node_name not in nodes.keys():
                nodes[node_name] = []
            nodes[node_name].append(node)
        return nodes

    def list_nested_catalogs(self):
        if len(self.nested_catalogs) != 0:
            for nc in self.nested_catalogs:
                print nc.getAttribute('xlink:title')
        else:
            print('There were no nested datasets found in the catalog.')

    def get_nested_catalog_links(self):
        from string import join
        links = []
        if len(self.nested_catalogs) != 0:
            for nc in self.nested_catalogs:
                catalog_url = join([self.base_tds_url,
                                    nc.getAttribute('xlink:href')], '')
                print catalog_url
        else:
            print('There were no nested datasets found in the catalog.')

class SimpleService():
    def __init__(self, serviceNode):
        self.name = serviceNode.attributes['name'].value
        self.serviceType = serviceNode.attributes['serviceType'].value
        self.base = serviceNode.attributes['base'].value

class TDSdataset():
    def __init__(self, rootNode, datasetNode):
        #
        # determine if dataset is direct or collection
        #
        has_datasets = len(datasetNode.getElementsByTagName('dataset')) != 0
        has_catalogRefs = len(datasetNode.getElementsByTagName('catalogRef')) != 0
        if (has_datasets or has_catalogRefs):
            self.type = 'collection'
        else:
            self.type = 'direct'

        self.name = datasetNode.attributes['name'].value
        #
        # Stuff in the metadata
        #
        self.metadata = datasetNode.getElementsByTagName('metadata')
        #
        # get services for the dataset
        #
        services = {'simple' : {}, 'compound' : {}}
        # check for root level service tags
        if isinstance(rootNode,TDSdataset):
            services = self.updateServiceDict(services, rootNode.services)
        else:
            for e in rootNode.childNodes:
                services = self.updateServiceDict(services, self.searchServiceTags(e))

        # look in metadata tags for service tags
        if self.metadata != []:
            for md in self.metadata:
                for e in md.childNodes:
                    services = self.updateServiceDict(services, self.searchServiceTags(e))

        self.services = services

        subdatasets = []
        if self.type == 'collection':
            for e in datasetNode.childNodes:
                if ((e.nodeType == e.ELEMENT_NODE) and (e.nodeName == 'dataset')):
                    subdatasets.append(TDSdataset(self, e))
        self.subdatasets = subdatasets

    def searchServiceTags(self, e):
        services = {'simple' : {}, 'compound' : {}}
        if ((e.nodeType == e.ELEMENT_NODE) and (e.nodeName == 'service')):
            if e.attributes['serviceType'] =='Compound':
                services['compound'][e.attributes['name'].value] = {}
                sub_service_nodes = e.getElementsByTagName('service')
                for ssn in sub_service_nodes:
                    services['compound'][e.attributes['name'].value] = SimpleService(ssn)
            else:
                services['simple'][e.attributes['name'].value] = SimpleService(e)

        return services

    def updateServiceDict(self, base_dict, new_dict):
        serviceTypes = ['simple','compound']
        for st in serviceTypes:
            for simkey in new_dict[st].keys():
                if base_dict[st].has_key(simkey):
                    raise NameError("Service already defined - must be unique!")

                base_dict[st][simkey] = new_dict[st][simkey]

        return base_dict

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Find all datasets on TDS server")
    parser.add_argument("-u", "--url", default=join([testServer,'thredds','catalog.xml'],'/'),
        help="url of the TDS catalog xml file you wish to begin crawling")
    args = parser.parse_args()

    cat = TDSCatalog(args.url)
    for ds in cat.datasets:
        print "main"
        print (ds.name, ds.type)

        for sds in ds.subdatasets:
            print "sub"
            print (sds.name, sds.type)

            for ssds in sds.subdatasets:
                print 'subsub'
                print (ssds.name, ssds.type)
    #for col in cat.datasets['collection']:
    #    print cat.datasets['collection'][col].toxml()
