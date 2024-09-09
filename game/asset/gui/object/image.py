import pygame
from pygame.sprite import AbstractGroup

from game.asset.conv import D2Position
import cv2

class ImageBase(pygame.sprite.Sprite):
    def __init__(self,position:D2Position, scale:int, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.position = position
        self.scale = scale


class JPG(ImageBase):
    def __init__(self, position: D2Position, scale:int, image:pygame.Surface, *groups: AbstractGroup) -> None:
        super().__init__(position, scale, *groups)
        self.image = image
    def draw(self,surface:pygame.Surface):
        rect = pygame.Rect(*self.position(),self.image.get_width()*self.scale,self.image.get_height()*self.scale)
        surface.blit(self.image,rect)

class GIF(ImageBase):
    @classmethod
    def GIF_LOAD(cls,FilePath):
        gif = cv2.VideoCapture(FilePath)
        images = []
        while True:
            scs,image = gif.read()
            if not scs:
                break
            images.append(image)
        return images
    def __init__(self, position: D2Position, fps:int, scale: int, *groups: AbstractGroup) -> None:
        super().__init__(position, scale, *groups)
        self.images = []
        self.index = 0
        self.fps = fps
        self.clock = pygame.time.Clock()
    def draw(self,surface:pygame.Surface):
        pass