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
    Generic error for a method that is not implemented yet
    '''
    def __init__(self, method, file_type):
        self.method = method
        self.file_type = file_type

    def __str__(self):
        return repr("Error: the {} method is not implemented for file type {}".format(self.method, self.file_type))

class UnexpectedFileTypeReturn(Exception):
    '''
    Generic error for a method that is not implemented yet
    '''
    def __init__(self, object, received):
        self.requested = object.return_file_type
        self.received = received

    def __str__(self):
        return repr("Error: Requested file type ({}) does not match received file type ({})!".format(self.requested,self.received))
