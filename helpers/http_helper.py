__all__ = ['basic_http_request', 'get_user_agent', 'get_timeout']

def get_user_agent():
    return 'pyTDSter'

def get_timeout(timeout_type = 'check'):
    '''
    get the default request timeout for pyTDSter (in seconds)
    '''
    if timeout_type == 'check':
        # Is server even running? 5 seconds
        return 5
    else:
        # 5 minutes
        return 300

def basic_http_request(full_url, return_response = False):
    import urllib2

    url_request = urllib2.Request(full_url)
    url_request.add_header('User-agent', get_user_agent())
    try:
        response = urllib2.urlopen(url_request)
        if return_response:
            return response
        else:
            del response
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: {}'.format(e.reason)
            print 'Full  url: {}'.format(full_url)
            raise
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: {}'.format(e.code)
            print 'TDS response: {}'.format(e.read())
            print 'Full  url: {}'.format(full_url)
            raise
        else:
            print 'error not caught!'
            raise