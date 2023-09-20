from app.config.types import Request_Type
from app.utils.makeCounter import makeCounter


counter = makeCounter()

class Encription_Request:
    def __init__(self, type = Request_Type.ENCRIPTION, service = 0):
        self.id = counter()
        self.type = type
        self.service = service
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        if id < 0:
            return
        self.__id = id
        
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, type):
        # if type < 0:
        #     return
        self.__type = type
        
    @property
    def service(self):
        return self.__service
    
    @service.setter
    def service(self, service):
        # if service < 0:
        #     return
        self.__service = service


