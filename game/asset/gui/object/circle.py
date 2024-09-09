import types
import pygame

from game.asset import scene,animation

class Circle(scene.SceneObject):
    def __init__(self,surface,radius):
        super().__init__(lambda: (0,0))
        self._animator = animation.Animation(animation.Easing.ease_out_expl,animation.Easing.ease_in_expl,0,200,800,500)
        self.__surface = surface
        self.radius = radius
    def test_motion(self,value):
        pygame.draw.circle(self.__surface,(0,0,0),(value,self.__surface.get_height()/2),self.radius)
