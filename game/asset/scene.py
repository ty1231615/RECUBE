import abc
from typing import Any
import pygame
import types
import threading
from game.asset.gui import event
from game.asset import color,conv,lang

class CameraRelation:
    def __init__(self,move_x=0,move_y=0,zoom_x=1,zoom_y=1):
        self.move_x = move_x
        self.move_y = move_y
        self.zoom_x = zoom_x
        self.zoom_y = zoom_y
    @property
    def surface(self):
        return self.__surface

def value_couping(*args):
    value = 0
    for _ in args:
        value += _
    return value

class Camera:
    CURRENT_CAMERA = None
    CURRENT_RELATION = CameraRelation()
    def __init__(self,cameraRelation:CameraRelation,surface:pygame.Surface):
        self.__position = cameraRelation
        self.__surface = surface
    @property
    def position(self):
        return self.__position
    @property
    def surface(self):
        return self.__surface
    @classmethod
    def setCurrent(cls,camera):
        if isinstance(camera,Camera):
            Camera.CURRENT_CAMERA = camera
            Camera.CURRENT_RELATION = camera.position
        else:
            raise ValueError()
    @classmethod
    def _X(cls,*args):
        return value_couping(*args) + Camera.CURRENT_RELATION.move_x
    @classmethod
    def _Y(cls,*args):
        return value_couping(*args) + Camera.CURRENT_RELATION.move_y
    @classmethod
    def SCALER(cls,surface:pygame.Surface):
        rect = surface.get_rect()
        return pygame.transform.scale(surface,(rect.width * Camera.CURRENT_RELATION.zoom_x,rect.height * Camera.CURRENT_RELATION.zoom_y))
    @classmethod
    def zoom_average(cls):
        return (Camera.CURRENT_RELATION.zoom_x+Camera.CURRENT_RELATION.zoom_y) / 2

#pageはシーンに対するキャンバスとして使う
class page:
    """
    This is the basic class of the page to be displayed in the scene
    """
    def __init__(self) -> None:
        self.__pages = []
    @property
    def pages(self):
        return self.__pages
    def add_page(self,scene):
        if isinstance(scene,Scene):
            self.pages.append(scene)
        else:
            raise ValueError
    def remove_page(self,index):
        self.pages.remove(index)

#
class OnePage(page):
    """
    Provides advanced operation by displaying only one page
    """
    def __init__(self):
        super().__init__()
        self.__now_page = 0
    @property
    def now_page(self):
        return self.__now_page
    def change_page(self,index:int,manager):
        self.__now_page = index
        if isinstance(manager,SceneManager):
            self.pages[self.__now_page].setup(manager)
    def draw_page(self,surface:pygame.Surface):
        self.pages[self.__now_page].render(surface)

class MultiPage(page):
    """
    Display multiple pages\n
    (one page is recommended)
    """
    def __init__(self):
        super().__init__()
    def draw_page(self,index:int,Surface:pygame.Surface,dest=(0,0)):
        Surface.blit(self.__pages[index],dest)

class Scene:
    """
    Create a game scene\n
    Inheriting a page allows you to expand another scene on top of the scene
    """
    def __init__(self,surface:pygame.Surface) -> None:
        self.__EVENT_HANDLER = event.EventHander()
        self.__surface = surface
        self.__TEXT_TOP = TextTop()
    @property
    def TEXT_TOP(self):
        return self.__TEXT_TOP
    @property
    def surface(self):
        return self.__surface
    @property
    def EVENT_HANDLER(self):
        return self.__EVENT_HANDLER
    def get_size_average(self):
        return (self.surface.get_width()+self.surface.get_height())/2
    def get_center(self):
        return (self.surface.get_width()/2,self.surface.get_height()/2)
    def setup(self,handler):
        raise NotImplementedError
    def update(self,events):
        raise NotImplementedError
    def render(self):
        #This function is supposed to be processed before the render function is executed
        self.__EVENT_HANDLER.CALL()
        self.__TEXT_TOP.draw_texts(self)

class SceneManager: #Manage scenes in bulk
    def __init__(self,camera) -> None:
        self.__camera = camera
        self.__scenes = []
        self.__current_scene:Scene = None
    @property
    def screen(self):
        return self.__screen
    @property
    def event_handler(self):
        return self.__event_handler
    @property
    def scenes(self):
        return self.__scenes
    @property
    def current_scene(self):
        return self.__current_scene
    def resize(self,size:tuple):
        self.__screen = pygame.display.set_mode(size)
        return self.__screen
    def add_scene(self, scene:Scene):
        self.scenes.append(scene)
    def change(self,scene):
        """
        Reflects the received scene object as is.
        However, it is recommended to make changes based on the index
        """
        if isinstance(scene,Scene):
            self.__current_scene = scene
            scene.setup(self)
        else:
            raise ValueError(scene)
    def change_scene(self, index):
        """
        Replace the received index with the current scene
        """
        self.current_scene = self.scenes[index]
        self.current_scene.setup(self)
    def update(self, events):
        self.current_scene.update(events)
    def render(self, surface):
        self.current_scene.render(surface)
    def RENDERING(self):
        """
        Draws the current scene.
        This function always does a while loop, so it is recommended to leave the necessary processing early.
        """
        while True:
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if Event.type == pygame.KEYDOWN:
                    event.InputEventHander.Input(Event.key)
            self.current_scene.render(self.__camera)
            pygame.display.flip()

class SceneObject:
    """
    Assumed to be inherited by objects displayed in the scene.\n
    Applies to event-related obj arguments.
    """
    def __init__(self,collideGetter:types.FunctionType): #Put the appropriate function in the collideGetter to get the hit
        self.__collider = collideGetter
    def draw(self,scene:Scene):
        raise NotImplementedError
    @property
    def collider(self):
        return self.__collider

#textが扱われる範囲
class TextTop:
    """
    TextBox handler.\n
    It is automatically created when a scene object is initialized.
    """
    def __init__(self):
        self.__texts = []
        self.__select = 0
    def off_forcus(self,textBox):
        if textBox in self.__texts:
            pass
        else:
            raise ValueError(f"{textBox} is not registered")
    def select(self,textBox):
        if isinstance(textBox,TextBox):
            self.__select = textBox
        else:
            raise TypeError("Pass the text box object")
    def draw_texts(self,SCENE:Scene):
        for instnace in self.__texts:
            instnace.draw(SCENE)
            instnace.event.update(0)
    def regit_text(self,text):
        if isinstance(text,TextBox):
            self.__texts.append(text)

def cut_string(string,p1,p2):
    return string[:p1] + string[p2:]

def insert_string(string,insert,index):
    return string[:index] + insert + string[index:]

class TextView(SceneObject):
    modes = [
        "center",
        "topleft",
        "topright",
        "bottomleft",
        "bottomright",
        "midtop",
        "midbottom",
        "midleft",
        "midright"
    ]
    def __init__(self,text,position:conv.D2Position,font:lang.VariableFont,mode:int,color:color.COLOR=color.text_color,antialias=False) -> Any:
        self._text_positon = position
        self._text_color = color
        self._text_style_font = font
        self._text_mode = TextView.modes[mode]
        self._text_antialias = antialias
        self._text_surface_colide = None
        self._text_surface = pygame.Surface((30,30))
        self.review(text,self._text_color,self._text_antialias)
    @property
    def _text_rect(self):
        return self._text_surface.get_rect(**{self._text_mode:self._text_positon()})
    def review(self,text:str,Color:color.COLOR,antialias=False):
        self._text_surface = self._text_style_font.Font().render(text,antialias,Color())
    def view(self):
        self._text_surface = Camera.SCALER(self._text_surface)
        self._text_surface_colide = self._text_surface.get_rect(**{self._text_mode:self._text_positon()})
        return (self._text_surface,self._text_surface_colide)

class TextBox(TextView):
    def __init__(self,top:TextTop,position,font:lang.VariableFont,defalt="",mode=0,text_color=color.text_color,line_color=color.text_color) -> None:
        self.__text = ""
        self.__before_text = "None"
        self.__defalt = defalt
        self.__forcus = False
        self.__each = True
        self.__select = 0
        self.__top = top
        self.__line_color = line_color
        self.__select_line_pos = [(0,0),(0,0)]
        self.line_margin = 10
        self.__textsData = [0]
        self.__event = event.ClickObjectEvent(
            self,
            conv.CycleDefine(
                self.forcus
            ),
            conv.CycleDefine(
                self.off_forcus
            )
        )
        self.__input_handler = event.InputEventHander()
        self.__input_handler.bind_function(self.input_text)
        super().__init__(self.__text,position,font,mode,text_color)
        SceneObject.__init__(self,lambda: self._text_surface.get_rect(**{self._text_mode:self._text_positon()}).collidepoint)
    @property
    def text_color(self):
        return self.__text_color
    @property
    def texts(self):
        return self.__text
    @property
    def text_mode(self):
        return self.__text_mode
    @property
    def event(self):
        return self.__event
    def text_render(self,text,color,antialias=False):
        return self._text_style_font.Font().render(text,antialias,color).get_width()
    def texts_render(self,texts,color,antialias=False):
        eachs = []
        befo = ""
        befo_value = self.line_margin
        for text in texts:
            befo_render = self.__font.Font().render(befo,antialias,color)
            after_render = self.__font.Font().render(befo+text,antialias,color)
            befo += text
            value = befo_value + after_render.get_width() - befo_render.get_width()
            eachs.append(
                value
            )
            befo_value = value
        eachs.append(
            befo_value + self.__font.Font().render(texts,antialias,color()).get_width() - eachs[-0]
        )
        return eachs
    def forcus(self):
        self.__forcus = True
        self.__each = True
    def off_forcus(self):
        self.__forcus = False
        self.__each = True
    def input_text(self,key):
        text = pygame.key.name(key)
        if self.__forcus:
            add_value = ""
            if key == pygame.K_BACKSPACE:
                if self.__select > 0:
                    self.__text = cut_string(self.__text,self.__select-1,self.__select)
                    self.__textsData.pop(self.__select)
                    self.__select -= 1
            elif key == pygame.K_RETURN:
                self.__forcus = False
            elif key == pygame.K_TAB:
                add_value += "  "
            elif key == pygame.K_SPACE:
                add_value += " "
            elif key == pygame.K_LEFT:
                self.__select -= 1
                if self.__select < 0:
                    self.__select = 0
            elif key == pygame.K_RIGHT:
                self.__select += 1
                if self.__select > len(self.__text):
                    self.__select = len(self.__text)
            else:
                if len(text) <= 1:
                    add_value = text
            self.__text = insert_string(self.__text,add_value,self.__select)
            data = self.text_render(add_value,self._text_color())
            self.__textsData.insert(self.__select,data)
            self.__select += len(add_value)
            self.__each = True
    def draw(self,SCENE:Scene):
        if self.__each:
            view_text = self.__text
            if not self.__text:
                if not self.__forcus:
                    view_text = self.__defalt
            self.review(view_text,self._text_color,True)
            rect = self._text_surface.get_rect()
            select_width = sum(self.__textsData[:self.__select])
            self.__select_line_pos = [
                (select_width+self.line_margin,0),
                (select_width+self.line_margin,rect.height+self.line_margin)
            ]
            self._text_surface = conv.surface_padding(self._text_surface,self.line_margin)
            rect = self._text_surface.get_rect()
            self._text_surface = Camera.SCALER(self._text_surface)
            self.__each = False
        if self.__forcus:
            pygame.draw.line(self._text_surface,self._text_color(),self.__select_line_pos[0],self.__select_line_pos[1],width=1)
        SCENE.surface.blit(*self.view())
