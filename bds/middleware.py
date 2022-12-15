from threading import current_thread

_REQUESTS = {}


class RequestNotFound(Exception):
    def __init__(self, message):
        self.message = message
        
        
class GetCurentUser:    
    def __get_request(self):
        thread = current_thread()
        if thread not in _REQUESTS:
            raise RequestNotFound('global request error')
        else:
            return _REQUESTS[thread]
        
    @property    
    def instance(self):
        request = self.__get_request()       
        return request.user  
    
    @property
    def staff_request(self):
        if self.instance.is_staff:
            return  self.__get_request()   
        return None


class RequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        _REQUESTS[current_thread()] = request

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)

        return response