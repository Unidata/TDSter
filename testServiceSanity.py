import pydap.lib
import json
import io
import os
from pydap.client import open_url
from string import join

from helpers import get_data_url, basic_http_request
from helpers import get_user_agent
from helpers.tdster_defaults import testServer, conf
from urllib2 import HTTPError
pydap.lib.USER_AGENT = get_user_agent()

__all__ = ["test_cdmremote", "test_ncss",
           "test_opendap", "test_http_server", "test_wms",
           "test_wcs", "test_iso", "test_uddc", "test_ncml",
           "test_rcv"]

def nciso_url_setup(testServer, service='iso'):
    iso_url = get_data_url(testServer, service=service)
    # create catalog url
    tmp = iso_url.replace('/iso/','/catalog/').split('/')
    tmp.pop()
    tmp = join(tmp,'/')
    catalog_req = join([tmp,'catalog.xml'],'/')
    dataset_req = iso_url.split('iso/')[-1]
    full_req = 'catalog={}&dataset={}'.format(catalog_req, dataset_req)
    full_url = join([iso_url, full_req], '?')
    return full_url

def test_cdmremote(testServer):
    cdmremote_request = 'req=form'
    cdmremote_url = get_data_url(testServer, service = 'cdmremote')
    full_url = join([cdmremote_url, cdmremote_request], '?')
    return basic_http_request(full_url, return_response = True)

def test_ncss(testServer):
    var = 'Temperature_height_above_ground'
    ncss_request = "var={}&temporal=all".format(var)
    ncss_url = get_data_url(testServer, service = 'ncss')
    full_url = join([ncss_url, ncss_request], '?')
    return basic_http_request(full_url, return_response = True)

def test_opendap(testServer):
    success = False
    full_url = get_data_url(testServer, service = 'odap')
    dataset = open_url(full_url)
    if len(dataset) != 0:
        success = True
    del dataset
    return success

def test_http_server(testServer):
    full_url = get_data_url(testServer, service = 'http')
    return basic_http_request(full_url, return_response = True)

def test_wms(testServer):
    wms_url = get_data_url(testServer, service = 'wms')
    wms_request = 'service=WMS&version=1.3.0&request=GetCapabilities'
    full_url = join([wms_url, wms_request],'?')
    return basic_http_request(full_url, return_response = True)

def test_wcs(testServer):
    wcs_url = get_data_url(testServer, service = 'wcs')
    wcs_request = 'service=WCS&version=1.0.0&request=GetCapabilities'
    full_url = join([wcs_url, wcs_request],'?')
    return basic_http_request(full_url, return_response = True)

def test_iso(testServer):
    full_url = nciso_url_setup(testServer, service='iso')
    return basic_http_request(full_url, return_response = True)

def test_uddc(testServer):
    full_url = nciso_url_setup(testServer, service='uddc')
    return basic_http_request(full_url, return_response = True)

def test_ncml(testServer):
    full_url = nciso_url_setup(testServer, service='ncml')
    return basic_http_request(full_url, return_response = True)

def test_rcv(testServer):
    tds_server = join([testServer,'thredds'],'/')
    service = 'remoteCatalogValidation.html'
    full_url = join([tds_server, service], '/')
    return basic_http_request(full_url, return_response = True)


def main(testServerUrl):
    # read in list of latest access urls, pick random one, test access urls
    testServer = testServerUrl
    results = {}
    for tst in __all__:
        try:
            response = eval(tst+'("{}")'.format(testServer))
            if type(response) is type(True):
                code = ""
                msg = "OK"
            else:
                code = response.code
                msg = response.msg
            results[tst] = [code, msg]
        except HTTPError, e:
            print e.code
            print e.reason
    for tst in results:
        print results[tst]

    testServerStr = testServer.replace("http",'').replace('.','-').replace('/','').replace(":","")
    serverStatus =  os.path.join(conf["reportOutputDirectory"], testServerStr + "_status.json")
    with io.open(serverStatus, 'w', encoding='utf-8') as f:
              f.write(unicode(json.dumps(results, ensure_ascii=False, indent=2)))

if __name__ == "__main__":
    for testServer in ["http://thredds.ucar.edu/", "http://thredds-test.unidata.ucar.edu/"]:
        main(testServer)
