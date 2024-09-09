import pickle
import types
import pygame
import copy
import inspect
import hashlib
from typing import Any
from game.asset import color

class Identification:
    def __init__(self) -> None:
        frame = inspect.currentframe().f_back
        if not frame:
            raise Exception("Incorrect class usage.")
        self.__base = str(frame.f_lineno) + str(frame.f_code.co_code) + str(frame.f_lasti)
        self.__id = hashlib.md5(self.__base.encode())
        #print(self.__base)
    @property
    def _id(self):
        return self.__id.hexdigest()
    @_id.setter
    def _id(self,value):
        return
    def __eq__(self, value: object) -> bool:
        return self._id == value
    def __ne__(self, value: object) -> bool:
        return self._id != value
    def __repr__(self) -> str:
        return self._id
    def __str__(self) -> str:
        return self._id
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.__id

class Pickler:
    def dump(self,path):
        pickle.dump(self,open(path,"wb"))
    @classmethod
    def load(cls,path):
        return pickle.load(open(path,"rb"))

class Configer:
    def __init__(self):
        self.__STRING_RELATION = {}
    def addRelation(self,string,ChangeDefine):
        self.__STRING_RELATION.update(
            {
                string:ChangeDefine
            }
        )
    def SetConfig(self,string,value):
        self.__STRING_RELATION.update({
            string:value
        })

class CycleDefine:
    def __init__(self,func:types.FunctionType,*arg,**kwarg) -> None:
        self.__arg = arg
        self.__kwarg = kwarg
        self.__function = func
    def __call__(self):
        self.__function(*self.__arg,**self.__kwarg)
    def change(self,*arg):
        self.__arg = arg
    def change(self,**kwarg):
        self.__kwarg = kwarg
    @property
    def define(self):
        return self.__function
    @property
    def arg(self):
        return self.__arg
    @property
    def kwarg(self):
        return self.__kwarg

def __surface_padding(surface:pygame.Surface,padding,**args):
    padding_surface = surface
    for _ in range(3):
        padding_surface = _surface_padding(padding_surface,_,padding,**args)
    return padding_surface

def rect_padding(rect,padding):
    new_rect = copy.deepcopy(rect)
    new_rect.left += padding
    new_rect.top += padding
    new_rect.width += padding
    new_rect.height += padding
    return new_rect

def byCenter_blit(surface:pygame.Surface,obj:pygame.Surface,pos:tuple):
    size = obj.get_size()
    return surface.blit(obj,(pos[0]-size[0]/2,pos[1]-size[1]/2))

def surface_padding(surface:pygame.Surface,padding):
    padded_width = surface.get_width() + 2 * padding
    padded_height = surface.get_height() + 2 * padding
    padded_surface = pygame.Surface((padded_width,padded_height),flags=surface.get_flags(),masks=surface.get_masks())
    padded_surface.blit(surface,(padding,padding))
    return padded_surface

def _surface_padding(surface:pygame.Surface,rotate:int,padding:int,**args):
    surface_width = surface.get_width()
    surface_height = surface.get_height()
    rotates = [
        (padding,0),
        (0,padding),
        (-padding,0),
        (0,-padding)
    ]
    select = rotates[rotate]
    padding_width = select[1]
    padding_height = select[0]
    loots = [
        (0,-padding),
        (0,0),
        (0,0),
        (padding,0)
    ]
    padding_surface = pygame.Surface((surface_width+padding_width,surface_height+padding_height),**args)
    padding_surface.blit(surface,loots[rotate])
    return padding_surface

class D2Position:
    def __init__(self,x,y) -> None:
        self.__x: int = x
        self.__y: int = y
    def __call__(self) -> Any:
        return (self.__x,self.__y)
    def _plusX(self,value):
        if self.__settter_base(value):
            return (self.__x + value,self.__y)
    def _plusY(self,value):
        if self.__settter_base(value):
            return (self.__x,self.__y + value)
    def plusX(self,value):
        if self.__settter_base(value):
            self.__x += int(value)
    def plusY(self,value):
        if self.__settter_base(value):
            self.__y += int(value)
    def __settter_base(self,value):
        if type(value) in [int,float]:
            return True
        return False
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,value):
        if self.__settter_base(value):
            self.__x = int(value)
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,value):
        if self.__settter_base(value):
            self.__y = int(value)

class Couping:
    def __init__(self,position:D2Position,parts) -> None:
        self.__parts = parts
        self.__positon = position
    def draw(self,surface):
        pass
    @property
    def parts(self):
        return self.__parts
    @property
    def parts(self,index):
        return self.__parts[index]
    @property
    def position(self):
        return self.__positon

class CoupingParts:
    def __init__(self,position:D2Position,obj):
        self.__obj = obj
        self.__position = position
    @property
    def obj(self):
        return self.__obj
    @property
    def position(self):
        return self.__position