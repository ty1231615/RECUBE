import sys,os

sys.path.append(f"{os.getcwd()}")

import pygame

from game.asset import scene,color,conv
from game.asset.package.stage import general,practice
from game.asset.package.player import handler
from game.asset.game import general as GameGeneral

pygame.init()

"""
mapStruct = general.MapStructure.generate_air_field(32)
blockData = general.Blocks(
    [
        "◈"
    ]
)
metaData = general.MapMetadata(
    mapStruct,blockData,25,blockAntiAlias=True
)
MapHandler = general.NormalMap(
    metaData,15,15,backgroundColor=color.COLOR(255,255,255)
)

class Mapview(GameGeneral.MapBase):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface,MapHandler)
    def setup(self, handler):
        handler.resize(self.surface.get_size())
    def render(self,camera:scene.Camera):
        self.surface.blit(self.mapHandler.draw(),(0,0))
        camera.surface.blit(self.surface,(0,0))

"""
screen = pygame.display.set_mode((1000,1000),pygame.RESIZABLE)
surface = pygame.Surface((1000,1000))
camera = scene.Camera(
    scene.CameraRelation(0,0,1,1),
    screen
)
scene.Camera.setCurrent(camera)
mapview = practice.PracticeGame(surface,[handler.Player(
    handler.PlayerControle(conv.D2Position(16,16)),
    handler.PlayerSide(handler.GameSide.SURVIVER),
    Scaling=30
)])

scene_manager = scene.SceneManager(camera)
scene_manager.change(mapview)
#
scene_manager.RENDERING()
#