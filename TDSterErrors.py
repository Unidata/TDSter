from helpers.tdster_defaults import testServer

__all__ = ['NotAnNcFileError', 'MethodNotImplementedForFileType', 'UnexpectedFileTypeReturn', 'NotAValidService']

class NotAnNcFileError(Exception):
    '''
    Exception class to indicate that a file cannot be opened as a netCDF file.
    '''
    def __init__(self, nc_file):
        self.value = nc_file

    def __str__(self):
        return repr("Error: {} is not a valid netCDF file".format(self.value))

class MethodNotImplementedForFileType(Exception):
    '''
    Generic error for a method that is not implemented for a specific file type
    '''
    def __init__(self, method, file_type):
        self.method = method
        self.file_type = file_type

    def __str__(self):
        return repr("Error: the {} method is not implemented for file type {}".format(self.method, self.file_type))

class UnexpectedFileTypeReturn(Exception):
    '''
    Error for the case when a request (like NCSS) returns a file that is different than what
    was requested (i.e. asked for .nc but got .xml instead).
    '''
    def __init__(self, object, received):
        self.requested = object.return_file_type
        self.received = received

    def __str__(self):
        return repr("Error: Requested file type ({}) does not match received file type ({})!".format(self.requested,self.received))

class NotAValidService(Exception):
    '''
    Error for the case where a url transform (from one service to another) is requesting a
    non-valid 'to_service'. Example: requsting a 'catalog' url to be transformed to an ncl
    url (this should be an ncml url, not ncl, thus the error). Also applies to the case where
    the to_url isn't specified.
    '''
    def __init__(self, valid_services, invalid_service):
        from string import join
        self.invalid_service = invalid_service
        self.valid_services = valid_services
        service_string = join(self.valid_services,', ')
        service_error = "Must submit a valid service to which you wish to "\
                        "transform the URL: choose from the following:{}".format(service_string)

        if self.invalid_service is not None:
            specific_message = "{} is not a valid service.".format(self.invalid_service)
            service_error = join([specific_message, service_error], ' ')

        self.service_error = service_error

    def __str__(self):
        return repr(self.service_error)

class CannnotReachThreddsServer(Exception):
    '''
    Exception class to indicate that a file cannot be opened as a netCDF file.
    '''
    def __init__(self, badServers, server_count):
        self.badServers = badServers
        self.server_count = server_count

    def __str__(self):
        print('{} severs tested'.format(self.server_count))
        print('Error - the following servers had errors:\n')
        for server in self.badServers.keys():
            print('{} : {}'.format(server, self.badServers[server]))


class StaleDatasetsDetected(Exception):
    '''
    Exception class to indicate that a file cannot be opened as a netCDF file.
    '''

    def __init__(self, report):
        self.testServer = testServer
        self.report = report

    def __str__(self):
        errorMsg = []
        errorMsg.append("Some of the datasets on {} are old:".format(testServer))
        for oldie in self.report:
            errorMsg.append("    " + oldie)
        errorMsg = "\n".join(errorMsg)
        return errorMsg