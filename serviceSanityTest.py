from string import join
from helpers import get_data_url, url_service_transform, basic_http_request

def test_cdmremote():
    cdmremote_request = 'req=form'
    cdmremote_url = get_data_url(service = 'cdmremote')
    full_url = join([cdmremote_url, cdmremote_request], '?')
    basic_http_request(full_url, return_response = False)

def test_ncss():
    var = 'Temperature_height_above_ground'
    ncss_request = "var={}&temporal=all".format(var)
    ncss_url = get_data_url(service = 'ncss')
    full_url = join([ncss_url, ncss_request], '?')
    basic_http_request(full_url, return_response = False)

def test_opendap():
    from pydap.client import open_url
    full_url = get_data_url(service = 'odap')
    dataset = open_url(full_url)
    del dataset

def test_http_server():
    full_url = get_data_url(service = 'http')
    basic_http_request(full_url, return_response = False)

def test_wms():
    wms_url = get_data_url(service = 'wms')
    wms_request = 'service=WMS&version=1.3.0&request=GetCapabilities'
    full_url = join([wms_url, wms_request],'?')
    basic_http_request(full_url, return_response = False)

def test_wcs():
    wcs_url = get_data_url(service = 'wcs')
    wcs_request = 'service=WCS&version=1.0.0&request=GetCapabilities'
    full_url = join([wcs_url, wcs_request],'?')
    basic_http_request(full_url, return_response = False)