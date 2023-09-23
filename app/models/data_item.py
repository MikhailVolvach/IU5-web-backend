from pathlib import Path

from app.utils.makeCounter import makeCounter

app_path = Path("../")

counter = makeCounter()

class DataItem:
    def __init__(self, img = "", title = "", path_to_file=""):
        self.__id = counter()
        self.img = img
        self.title = title
        self.data = path_to_file
        
    @property
    def id(self):
        return self.__id
    
    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, img):
        # if not isinstance(img, ):
        #     return
        
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
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, path_to_file):
        try:
            with open(path_to_file, 'r', encoding='utf-8') as f:
                self.__data = f.read(1000)
        except:
            print("Error, cannot open file", path_to_file)
            