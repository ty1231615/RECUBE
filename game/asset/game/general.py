import pygame

from game.asset.package.stage import general
from game.asset import scene

class MapBase(scene.Scene):
    def __init__(self,surface:pygame.Surface,MapHandler:general.Map) -> None:
        super().__init__(surface)
        self.__mapHandler = MapHandler
    def render(self):
        raise NotImplementedError
    def setup(self,handler):
        return handler
    @property
    def mapHandler(self):
        return self.__mapHandler

class GameBase(scene.Scene):
    def __init__(self,surface:pygame.Surface,stage:MapBase,players,texture:general.Blocks) -> None:
        super().__init__(surface)
        self.stage = stage
        self.players = players
        self.texture = texture
        self.model = []
    def setup(self, handler):
        pass
    def render(self,camera:pygame.Surface):
        return camera