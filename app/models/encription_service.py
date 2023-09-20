from app.utils.makeCounter import makeCounter
counter = makeCounter()

class Encription_Service:
    def __init__(self, img = "", title = "", description = "", cost = 0):
        self.id = counter()
        self.img = img
        self.title = title
        self.description = description
        self.cost = cost
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        if id < 0:
            return
        self.__id = id
    
    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, img):
        if not isinstance(img, str):
            return
        self.__img = img
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            return
        self.__title = title
    
    @property
    def cost(self):
        return self.__cost
    
    @cost.setter
    def cost(self, cost):
        if cost < 0:
            return
        self.__cost = cost
    
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            return
        self.__description = description