import pygame

from game.asset import color,scene
from game.asset.game import general
from game.asset.package.stage import general as mapKit
from game.asset.package.player import handler

texture = mapKit.Blocks(["▲","■"])

class PracticePlayer(handler.PlayerControleRule):
    def __init__(self, impassableBlocks: list, goalBlock: int, speed: int = 1) -> None:
        super().__init__(impassableBlocks, goalBlock, speed)

class PracticeGame(general.GameBase):
    def __init__(self, surface:pygame.Surface, players:list) -> None:
        STRUCT = mapKit.MapStructure.generate_air_field(25)
        stage = general.MapBase(
            surface,
            mapKit.NormalMap(
                mapKit.MapMetadata(
                    STRUCT,
                    mapKit.Blocks(["◈","■"]),
                    25,
                    True
                ),
                15,15,
                color.COLOR(255,255,255)
            )
        )
        super().__init__(surface, stage, players, texture)
        self.model = texture.generateBlocksData(
            stage.mapHandler.blockWidth+self.players[0].scaling,
            stage.mapHandler.blockWidth+self.players[0].scaling,
            True,
            customColor={
                1:players[0].loadColor()
            }
        )
        self.stage.mapHandler.metaData.map_struct.hold_over_around()
        self.players[0].model = self.model[1]
        self.players[0].controle.mapData = stage.mapHandler.metaData.map_struct
        self.players[0].binded = True
    def setup(self, handler):
        handler.resize(self.surface.get_size())
    def draw_players(self,surface):
        for player in self.players:
            x = self.stage.mapHandler.get_positionX(player.controle.position.x)
            y = self.stage.mapHandler.get_positionY(player.controle.position.y)
            surface.blit(player.model,(x-player.scaling/2,y-player.scaling/2))
    def render(self,camera:scene.Camera):
        gameSurface = self.stage.mapHandler.draw()
        self.draw_players(gameSurface)
        self.surface.blit(gameSurface,(0,0))
        camera.surface.blit(self.surface,(0,0))