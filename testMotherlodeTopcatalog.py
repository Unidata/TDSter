from catalogTDS import TDSCatalog
from string import join
from helpers.tdster_defaults import testServer
from TDSterErrors import CannnotReachThreddsServer

def test_topcatalog_servers():
    import urllib2

    from helpers import get_user_agent, get_timeout

    user_agent = get_user_agent()
    timeout = get_timeout()

    cat_url = join([testServer,'thredds','topcatalog.xml'],'/')
    cat = TDSCatalog(cat_url)
    badServers = {}
    server_count = 0
    topCatalogServers = cat.catalogRefs.keys()
    for server in topCatalogServers:
        server_count += 1
        test_url = cat.catalogRefs[server].href
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

            badServers[test_url] = error_info
            del error_info
            pass

    if badServers.keys() != []:
        raise CannnotReachThreddsServer(badServers, server_count)
