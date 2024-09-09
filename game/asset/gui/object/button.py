import pygame

from game.asset.scene import TextView,SceneObject
from game.asset.conv import D2Position,surface_padding,rect_padding,CycleDefine
from game.asset.lang import VariableFont
from game.asset.color import COLOR
from game.asset.gui import event

class ButtonBase(TextView):
    def __init__(self,d2position:D2Position,font:VariableFont,mode:int,text:str,color:COLOR,backgroundColor:COLOR,padding=10,Click=None,ClickOut=None,onCollition=None,onCollitionOut=None,clickSelect=0,set_alpha=False) -> None:
        self.padding = padding
        self.alpha_value = set_alpha
        self.text = text
        self.click_select = clickSelect
        self.position = d2position
        self.background_color = backgroundColor
        self.background_surface = pygame.Surface((0,0))
        super().__init__(self.text,self.position,font,mode,color)
        self.review(self.text,color,antialias=True)
        self.text_surface = self.view()
        self.redraw()
        SceneObject.__init__(self,lambda: rect_padding(
            self._text_rect
            ,self.padding
        ).collidepoint)
        if not Click:
            Click = self.Click
        if not ClickOut:
            ClickOut = self.ClickOut
        if not onCollition:
            onCollition = self.onCollision
        if not onCollitionOut:
            onCollitionOut = self.onOutCollision
        self.onButtonHandler = event.CD_ObjectEvent(
            self,
            CycleDefine(onCollition),
            CycleDefine(onCollitionOut)
        )
        self.buttonClickHandler = event.ClickObjectEvent(
            self,
            CycleDefine(Click),
            CycleDefine(ClickOut)
        )
    def onCollision(self):
        return True
    def onOutCollision(self):
        return True
    def Click(self):
        return True
    def ClickOut(self):
        return True
    def redraw(self):
        self.text_surface = self.view()
        self.background_surface = surface_padding(self.text_surface[0],self.padding)
        if not self.alpha_value:
            self.background_surface.fill(self.background_color())
    def draw(self):
        self.buttonClickHandler.update(self.click_select)
        return surface_padding(self.text_surface[0],self.padding)

class SimpleButton(ButtonBase):
    def __init__(self, d2position: D2Position, font: VariableFont, mode: int, text: str, color: COLOR, backgroundColor, padding=10, LineWidth=3, LineColor=COLOR(0,0,0),Click=None,ClickOut=None,onCollition=None,onCollitionOut=None,clickSelect=0,set_alpha=False) -> None:
        super().__init__(d2position, font, mode, text, color, backgroundColor, padding,Click,ClickOut,onCollition,onCollitionOut,clickSelect,set_alpha=set_alpha)
        self.line_color = LineColor
        self.line_width = LineWidth
        self.rect = self._text_rect
    def flame_view(self,surface:pygame.Surface):
        height = surface.get_height()
        width = surface.get_width()
        #flame line
        pygame.draw.line(surface,self.line_color(),(0,0),(width,0),self.line_width)
        pygame.draw.line(surface,self.line_color(),(0,height),(width,height),self.line_width)
        pygame.draw.line(surface,self.line_color(),(0,0),(0,height),self.line_width)
        pygame.draw.line(surface,self.line_color(),(width,0),(width,height),self.line_width)
        return surface
    def draw(self,visual:pygame.Surface):
        surface = self.flame_view(super().draw())
        self.background_surface.blit(surface,(0,0))
        self.rect = rect_padding(self._text_rect,self.padding)
        visual.blit(self.background_surface,self.rect)