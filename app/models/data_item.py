from os import listdir, walk
from pathlib import Path

from app.utils.makeCounter import makeCounter

app_path = Path("../")

counter = makeCounter()

class DataItem:
    def __init__(self, img = "", title = "", value="", is_file=False, is_iterable=False):
        self.__id = counter()
        self.img = img
        self.title = title
        self.is_file = is_file
        self.is_iterable = is_iterable
        self.data = value
        
    @property
    def id(self):
        return self.__id
    
    @property
    def img(self):
        return self.__img
    
    @img.setter
    def img(self, img):        
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
    def data(self, value):
        if not isinstance(value, Path):
            return
        
        if (self.is_file):
            if self.is_iterable:
                try:
                    files = listdir(value[:value.rindex('/')])
                    self.__data = [file for file in files if value in files]
                except:
                    print("Error, cannot open directory", value)
            try:
                # print()
                with open(value, 'r', encoding='utf-8') as f:
                    self.__data = f.read(1000) + "..."
            except:
                print("Error, cannot open file", value)
        else:
            try:
                files = listdir(value)
                self.__data = files
            except:
                print("Error, cannot open directory", value)
    
    @property
    def is_file(self):
        return self.__is_file
    
    @is_file.setter
    def is_file(self, new_is_file):
        if (new_is_file not in [0, 1]):
            return
        self.__is_file = new_is_file
        
    @property
    def is_iterable(self):
        return self.__is_iterable
    
    @is_iterable.setter
    def is_iterable(self, new_is_iterable):
        if (new_is_iterable not in [0, 1]):
            return
        self.__is_iterable = new_is_iterable
