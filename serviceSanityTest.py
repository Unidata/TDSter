from string import join
from helpers import get_data_url, url_service_transform, basic_http_request
import urllib2

def test_cdmremote():
    cdmremote_url = get_data_url(service = 'cdmremote')
    full_url = join([cdmremote_url, 'req=form'], '?')
    basic_http_request(full_url)

def test_ncss():
    var = 'Temperature_height_above_ground'
    basic_ncss_request = "var={}&temporal=all".format(var)
    ncss_url = get_data_url(service = 'ncss')
    full_url = join([ncss_url, basic_ncss_request], '?')
    basic_http_request(full_url)

def test_http_server():
    full_url = get_data_url(service = 'http')
    basic_http_request(full_url)