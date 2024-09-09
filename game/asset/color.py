from typing import Any


class COLOR:
    def __init__(self,r,g,b) -> None:
        self.__r = r
        self.__g = g
        self.__b = b
    def __call__(self,index=0):
        color = [
            self.r,
            self.g,
            self.b
        ]
        if index == 0:
            return (self.r,self.g,self.b)
        elif index > 0:
            return color[index-1]
    @property
    def r(self):
        return self.__r
    @r.setter
    def r(self,value):
        self.__r = value
        if value > 255:
            self.__r = 255
    @property
    def g(self):
        return self.__g
    @g.setter
    def g(self,value):
        self.__g = value
        if value > 255:
            self.__g = 255
    @property
    def b(self):
        return self.__b
    @b.setter
    def b(self,value):
        self.__b = value
        if value > 255:
            self.__b = 255

home_color = COLOR(209, 209, 209)
login_canvas_color = COLOR(163, 191, 255)
text_color = COLOR(43, 49, 59)