from catalogTDS import TDSCatalog

def test_topcatalog_servers():
    import urllib2

    from helpers import get_user_agent, basic_http_request, get_timeout

    user_agent = get_user_agent()
    timeout = get_timeout()

    cat_url = 'http://motherlode.ucar.edu:8080/thredds/topcatalog.xml'
    cat = TDSCatalog(cat_url)
    remove_list = {}
    server_count = 0
    for nested_catalog in cat.nested_catalogs:
        server_count += 1
        test_url = nested_catalog.attributes['xlink:href'].value
        url_request = urllib2.Request(test_url)
        url_request.add_header('User-agent', user_agent)
        try:
            response = urllib2.urlopen(url_request, timeout = timeout)
        except IOError, e:
            error_info = 'Missing...something *did* go wrong with the error checking!'
            if hasattr(e, 'reason'):
                error_info = e.reason
            elif hasattr(e, 'code'):
                error_info = e.code
            elif hasattr(e, 'args'):
                if 'timed out' in e.args:
                    error_info = "timed out"
                else:
                    print 'error not caught!'
                    raise
            else:
                print 'error not caught!'
                raise

            remove_list[test_url] = error_info
            del error_info
            pass

    if remove_list.keys() != []:
        print('{} severs tested'.format(server_count))
        print('Error - the following servers had errors:\n')
        for server in remove_list.keys():
            print('{} : {}'.format(server, remove_list[server]))
            raise NameError('Check These Servers!!!')
