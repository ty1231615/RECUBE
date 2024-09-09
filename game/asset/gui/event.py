import pygame
import abc
import time

from game.asset import conv

class Event(metaclass=abc.ABCMeta):
    def __init__(self,obj,trigger:conv.CycleDefine,OffTrigger:conv.CycleDefine=None):
        self.__obj = obj
        self.__TRIGGER = trigger
        self.__OFF_TRIGGER = OffTrigger
    def update(self) -> bool:
        raise NotImplementedError
    @property
    def OFF_TRIGGER(self):
        return self.__OFF_TRIGGER
    @property
    def TRIGGER(self):
        return self.__TRIGGER
    @property
    def obj(self):
        return self.__obj

class EventHander:
    def __init__(self) -> None:
        self.__EVENTS = []
    @property
    def Scene(self):
        return self.__Scene
    def add_event(self,*event:Event):
        self.__EVENTS.append(*event)
    def remove_event(self,index):
        self.__EVENTS.pop(index)
    def CALL(self):
        for EVE in self.__EVENTS:
            EVE.update()

class Collider(metaclass=abc.ABCMeta):
    def collition(self):
        raise NotImplementedError

class MouseOneClick:
    def __init__(self) -> None:
        self.__clicked = False
        self.__returned = False
    def pressed(self):
        state = pygame.mouse.get_pressed()
        self.__clicked = any(state)
        if self.__clicked:
            if not self.__returned:
                self.__returned = True
                return state         
        if not self.__clicked:
            self.__returned = False
        return (False,False,False)

class CD_ObjectEvent(Event):
    def __init__(self, obj, trigger: conv.CycleDefine, OffTrigger: conv.CycleDefine = None):
        super().__init__(obj, trigger, OffTrigger)

class ClickObjectEvent(Event):
    """
    Event when an object is clicked
    """
    def __init__(self, obj, trigger: conv.CycleDefine, OffTrigger: conv.CycleDefine = None):
        super().__init__(obj, trigger, OffTrigger)
        self.__ONE_CLICK = MouseOneClick()
    def update(self,selectState):
        """
        selectState specifies the index of the target mouse status\n
        (As an example, the left click is detected in case of number 0)
        """
        if self.__ONE_CLICK.pressed()[selectState]:
            if self.obj.collider()(pygame.mouse.get_pos()):
                self.TRIGGER()
            else:
                if self.OFF_TRIGGER:
                    self.OFF_TRIGGER()

class InputEventHander:
    _REGIT = []
    def __init__(self) -> None:
        self.__binds = []
        if not self in InputEventHander._REGIT:
            InputEventHander._REGIT.append(self)
    @property
    def binds(self):
        return self.__binds
    def __del__(self):
        if self in InputEventHander._REGIT:
            InputEventHander._REGIT.remove(self)
    @classmethod
    def Input(cls,key):
        for instance in InputEventHander._REGIT:
            if type(instance) is InputEventHander:
                for func in instance.binds:
                    if func:
                        func(key)
                    else:
                        InputEventHander._REGIT.remove(func)
    def bind_function(self,func):
        self.__binds.append(
            lambda key:func(key)
        )
