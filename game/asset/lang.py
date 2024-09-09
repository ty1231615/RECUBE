import pygame

class Lang:
    def __init__(self,langNumber:int,value:str) -> None:
        self.__langnumber = langNumber
        self.__value = value
        if not langNumber in Phrase.lang:
            raise ValueError("Unregistered language number is used")
    @property
    def langNumber(self):
        return self.__langnumber
    @property
    def value(self):
        return self.__value

class Phrase:
    _jp = 0
    _en = 1
    lang = [
        _jp,
        _en
    ]
    def __init__(self,defalt,*lang) -> None:
        self.__phrases = []
        self.__defalt = defalt
        self.add(*lang)
    def get_phrase(self,langNumber):
        for phrase in self.__phrases:
            if phrase.langNumber == langNumber:
                return phrase
    def add(self,*lang):
        for _ in lang:
            if isinstance(_,Lang):
                self.__phrases.append(_)
            else:
                raise ValueError("Please put the lang object")
    @property
    def phrase(self):
        return self.__phrases

class Texts:
    def __init__(self) -> None:
        self.__phrases = []
    def add(self,*phrase:Phrase):
        for _ in phrase:
            if isinstance(_,Phrase):
                self.__phrases.append(_)
            else:
                raise ValueError("Please put the phrase object")
    def get_phrase(self,index:int,langNumber:int):
        return self.get(index).get_phrase(langNumber)
    def get(self,index):
        return self.__phrases[index]

class VariableFont:
    def __init__(self,path,size) -> None:
        self.__path = path
        self.__size = size
        self.__change = False
        self.__temp = self.get_font()
    @property
    def size(self):
        return self.__size
    @property
    def path(self):
        return self.__path
    def ChangeSize(self,size):
        self.__change = True
        self.__size = size
    def get_font(self):
        return pygame.font.Font(self.__path,int(self.__size()))
    def Font(self):
        if self.__change:
            self.__temp = self.get_font()
            self.__change = False
        return self.__temp