import pygame
from game.asset import scene,conv,lang,color,setting
from enum import Enum

class BlockID(Enum):
    AIR = 1
    WALL = 2

class Blocks:
    def __init__(self,objs:list) -> None:
        self.__relation = [","] + objs
    @classmethod
    def defalt_customModel(self):
        return {
            BlockID.WALL.value:{}
        }
    def get_index(self,index,defalt=0):
        try:
            value = self.__relation[index]
        except ValueError:
            value = self.__relation[defalt]
        return value
    @property
    def relation(self):
        return self.__relation
    def generateBlocksData(self,width,height,antialias=False,color=color.COLOR(0,0,0),background=None,customColor:dict={}):
        data = []
        base_color = color
        render_font = pygame.font.Font(setting.FONTS[4],int((width+height)/2))
        for index in range(len(self.__relation)):
            color = base_color
            if index in customColor:
                color = customColor[index]
            data.append(self.generateView(index,render_font,width,height,antialias,color,background))
        return data
    def generateView(self,index,Font:pygame.font.Font,width,height,antialias=False,color=color.COLOR(0,0,0),background=None):
        text = self.get_index(index)
        text_surface = Font.render(text,antialias,color(),background)
        return pygame.transform.scale(text_surface,(width,height))

class MapStructure:
    @classmethod
    def generate_air_field(cls,size):
        return MapStructure(
            [
                *[[BlockID.AIR] * size] * size
            ]
        )
    def __init__(self,struct) -> None:
        self.__MAPS = struct
        self.width,self.height = self.get_max_width_height()
    def get_max_width_height(self):
        height = len(self.__MAPS)
        width = 0
        for line in self.__MAPS:
            count = len(line)
            if count > width:
                width = count
        return (width,height)
    def hold_over_around(self):
        for i in range(0,len(self.__MAPS)):
            if i in [0,len(self.__MAPS)-1]:
                width = len(self.__MAPS[i])
                self.__MAPS[i] = [*[BlockID.WALL] * width]
            self.__MAPS[i][0] = BlockID.WALL
            self.__MAPS[i][-1] = BlockID.WALL
    @property
    def structure(self):
        return self.__MAPS

class MapMetadata:
    def __init__(self,map_spec:MapStructure,blocksData:Blocks,padding:float,blockAntiAlias=True,blockColor=color.COLOR(0,0,0),BlockBackground=None) -> None:
        self.__block = blocksData
        self.__padding = padding
        self.__map_spec = map_spec
        self.__blockAntiAlias = blockAntiAlias
        self.__blockColor = blockColor
        self.__blockBackground = BlockBackground
    @property
    def blockAntiAlias(self):
        return self.__blockAntiAlias
    @property
    def blockColor(self):
        return self.__blockColor
    @property
    def blockBackground(self):
        return self.__blockBackground
    @property
    def block(self):
        return self.__block
    @property
    def padding(self):
        return self.__padding
    @property
    def map_struct(self):
        return self.__map_spec

class Map:
    def __init__(self,metadata:MapMetadata,width:int,height:int,backgroundColor:color.COLOR) -> None:
        self.__metaData = metadata
        self.blockWidth = width
        self.blockHeight = height
        self.backgroundColor = backgroundColor
        MapStruct = self.metaData.map_struct
        self.draw_surface = pygame.Surface((MapStruct.width * self.blockWidth + self.metaData.padding * MapStruct.width,MapStruct.height * self.blockHeight + self.metaData.padding * MapStruct.height))
    def get_positionX(self,index):
        return ((self.metaData.padding + self.blockWidth) * index) + self.blockWidth
    def get_positionY(self,index):
        return ((self.metaData.padding + self.blockHeight) * index) + self.blockHeight
    @property
    def metaData(self):
        return self.__metaData
    def draw(self) -> pygame.Surface:
        raise NotImplementedError

class NormalMap(Map):
    def __init__(self, metadata,width,height,*args,**kwargs) -> None:
        super().__init__(metadata,width,height,*args,**kwargs)
        self.blocks = self.metaData.block.generateBlocksData(self.blockWidth,self.blockHeight,self.metaData.blockAntiAlias,self.metaData.blockColor,self.metaData.blockBackground)
    def draw(self):
        MapStruct = self.metaData.map_struct
        self.draw_surface.fill(self.backgroundColor())
        for l_,line in enumerate(MapStruct.structure):
            pady = self.get_positionY(l_)
            for b_,block in enumerate(line):
                padx = self.get_positionX(b_)
                self.draw_surface.blit(self.blocks[block.value],(padx,pady))
        return self.draw_surface


