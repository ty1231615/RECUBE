import grpc
import pygame


from game.asset import scene,setting,conv,lang,color
from game.asset.package import login
from game.asset.gui.object import button

class TitlePage(scene.Scene):
    def __init__(self,surface:pygame.Surface) -> None:
        super().__init__(surface)
        self.langs = lang.Texts()
        self.langs.add(
            lang.Phrase(
                "play",
                lang.Lang(0,"p l a y"),
                lang.Lang(1,"P l a y")
            ),
            lang.Phrase(
                "multi",
                lang.Lang(0,"o n l i n e"),
                lang.Lang(1,"O n l i n e")
            ),
            lang.Phrase(
                "exit",
                lang.Lang(0,"e x i t"),
                lang.Lang(1,"E x i t")
            )
        )
        self.title_text = scene.TextView("R E C U B E",conv.D2Position(self.surface.get_width()/2,self.surface.get_height() / 5),font=lang.VariableFont(setting.DEFALT_FONT_PATH,lambda:self.get_size_average()/8),mode=0,color=color.COLOR(255,255,255))
        self.play_button = button.SimpleButton(conv.D2Position(self.surface.get_width()/2,self.surface.get_height() * 0.45),font=lang.VariableFont(setting.FONTS[1],lambda:self.get_size_average()/13),mode=0,text=self.langs.get_phrase(0,setting.LANG_NUMBER).value,color=color.COLOR(255,255,255),backgroundColor=color.COLOR(0,0,0),LineWidth=0,padding=0,set_alpha=True)
        self.multi_button = button.SimpleButton(conv.D2Position(self.surface.get_width()/2,self.surface.get_height() * 0.6),font=lang.VariableFont(setting.FONTS[1],lambda:self.get_size_average()/13),mode=0,text=self.langs.get_phrase(1,setting.LANG_NUMBER).value,color=color.COLOR(255,255,255),backgroundColor=color.COLOR(0,0,0),LineWidth=0,padding=0,set_alpha=True)
        self.exit_button = button.SimpleButton(conv.D2Position(self.surface.get_width()/2,self.surface.get_height() * 0.75),font=lang.VariableFont(setting.FONTS[1],lambda:self.get_size_average()/13),mode=0,text=self.langs.get_phrase(2,setting.LANG_NUMBER).value,color=color.COLOR(255,255,255),backgroundColor=color.COLOR(0,0,0),LineWidth=0,padding=0,set_alpha=True,Click=lambda: quit())
    def setup(self,handler:scene.SceneManager):
        handler.resize(setting.HOME_SIZE)
    def render(self,surface:pygame.Surface):
        super().render()
        self.surface.blit(pygame.image.load(setting.HOME_IMAGE_PATH),(0,0))
        self.surface.blit(*self.title_text.view())
        self.play_button.draw(self.surface)
        self.multi_button.draw(self.surface)
        self.exit_button.draw(self.surface)
        surface.blit(self.surface,(scene.Camera._X(),scene.Camera._Y()))

class PlayPage(scene.Scene):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface)
    def render():
        super().render()
    def setup(self,handler:scene.SceneManager):
        handler.resize(setting.HOME_SIZE)

class Home(scene.Scene,scene.OnePage):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface)
        super(scene.OnePage,self).__init__()
        self.add_page(TitlePage(surface))
    def setup(self,handler:scene.SceneManager):
        handler.resize(setting.HOME_SIZE)
    def render(self,camera:scene.Camera):
        super().render()
        self.draw_page(camera.surface)


