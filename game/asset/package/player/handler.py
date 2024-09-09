import pygame
import math

from game.asset import conv,lang,setting,color
from game.asset.conv import Identification
from game.asset.gui import event
from game.asset.package.player import advantage
from game.asset.package.stage import general
from game import logger
from enum import Enum

class GameSide(Enum):
    SURVIVER = Identification()
    HUNTER = Identification()
_COLOR = {
    GameSide.SURVIVER:color.COLOR(*setting.NORMAL_PLAYER_COLOR["SURVIVER"]),
    GameSide.HUNTER:color.COLOR(*setting.NORMAL_PLAYER_COLOR["HUNTER"])
}

class PlayerSide:
    #under development
    SURVIVER_DESCRIPTION = lang.Texts()
    SURVIVER_DESCRIPTION.add(
        lang.Phrase("surviver",lang.Lang(0,"あなたはサバイバーです"),lang.Lang(1,"you are Surviver")),
        lang.Phrase("hunter",lang.Lang(0,"あなたはハンターです"),lang.Lang(1,"you are Hunter"))
    )
    @classmethod
    def description(cls,index,lang=0):
        return PlayerSide.SURVIVER_DESCRIPTION.get_phrase(index,lang)
    def __init__(self,side:GameSide) -> None:
        self.__side = side
        if side.value in GameSide._member_map_.values():
            raise TypeError()
    @property
    def side(self):
        return self.__side

class Player:
    def __init__(self,controle,playerSide:PlayerSide,model=pygame.Surface((10,10)),Scaling=0):
        self.controle = controle
        self.team = playerSide
        self.model = model
        self.scaling = Scaling
    def loadColor(self):
        return _COLOR[self.team.side]

class PlayerMoveReason(Enum):
    NoReason = 0
    ByTheKey = 1
    AutoPilot = 2
    NoApprove = 3

class PlayerControleRule:
    def __init__(self,impassableBlocks:list,goalBlock:int,speed:int=1) -> None:
        self.__impassableBlockIds = impassableBlocks
        self.__goalBlockId = goalBlock
        self.__movement_range = speed
    def _check_movement(self,From:conv.D2Position,To:conv.D2Position):
        distance = math.sqrt(math.pow(From.x - To.x,2) + math.pow(From.y - To.y,2))
        if int(distance) == self.__movement_range:
            return True
        else:
            return False
    @classmethod
    def DefaltPreset(cls):
        return PlayerControleRule([0],0,1)
    @property
    def goalBlockId(self):
        return self.__goalBlockId
    @property
    def impassableBlockIds(self):
        return self.__impassableBlockIds

class PlayerControle:
    def __init__(self,position: conv.D2Position,controleRule:PlayerControleRule=PlayerControleRule.DefaltPreset()):
        self.position = position
        self.__binded = False
        self.__mapData = None
        self.__controleRule = controleRule
        self.inputEventBind = event.InputEventHander()
        self.inputEventBind.bind_function(self.AbstractKeyReciver)
    def setControleRule(self,controleRule:PlayerControleRule):
        if isinstance(controleRule,PlayerControleRule):
            self.__controleRule = controleRule
    def setMoveFunction(self,approve:bool,newLocation:conv.D2Position,reason:PlayerMoveReason):
        logger.system_log.warning("Function is called without being overridden",exc_info=True)
    @property
    def controleRule(self):
        return self.__controleRule
    @property
    def mapData(self):
        return self.__mapData
    @mapData.setter
    def mapData(self,value):
        if type(value) is general.MapStructure:
            self.__mapData = value
        else:
            raise TypeError()
    @property
    def binded(self):
        return self.__binded
    @binded.setter
    def binded(self,value):
        if type(value) is bool:
            self.__binded = value
    def AbstractKeyReciver(self,key):
        if not self.binded:
            base_position = self.position()
            new_position = (0,0)
            if key == pygame.K_UP or key == pygame.K_w:
                new_position = self.up()
            elif key == pygame.K_DOWN or key == pygame.K_s:
                new_position = self.down()
            elif key == pygame.K_LEFT or key == pygame.K_a:
                new_position = self.left()
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                new_position = self.right()
            #print(self.position.x,self.position.y)
            if self.controleRule._check_movement(conv.D2Position(*base_position),conv.D2Position(*new_position)):
                return self.setMoveFunction(True,new_position,PlayerMoveReason.ByTheKey)
            else:
                return self.setMoveFunction(False,base_position,PlayerMoveReason.NoApprove)
        return self.setMoveFunction(False,(0,0),PlayerMoveReason.NoReason)
    def up(self,speed=1):
        if self.mapData.height + speed > self.mapData.height:
            return self.position._plusY(-speed)
    def down(self,speed=1):
        if self.mapData.height - speed < self.mapData.height:
            return self.position._plusY(speed)
    def right(self,speed=1):
        if self.mapData.width + speed > self.mapData.width:
            return self.position._plusX(speed)
    def left(self,speed=1):
        if self.mapData.width - speed < self.mapData.width:
            return self.position._plusX(-speed)