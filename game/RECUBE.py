import sys,os

sys.path.append(f"{os.getcwd()}")

import threading
import pygame
import asyncio
from game.asset import setting
from game.asset import scene
from game.asset.package import login,home
from game.asset.gui import event
from game.asset.gui.object import image

pygame.init()

def go_login(success_flag=None):
    login_scene = login.LoginScene(success_flag=success_flag)
    SCENE_MANAGER.change(login_scene)
    login_scene.change_page(0,SCENE_MANAGER)
    return login_scene

def go_home(surface:pygame.Surface):
    home_scene = home.Home(surface)
    SCENE_MANAGER.change(home_scene)
    home_scene.change_page(0,SCENE_MANAGER)
    return home_scene

screen = pygame.display.set_mode(setting.LOAD_SIZE,pygame.RESIZABLE)
camera = scene.Camera(
    scene.CameraRelation(0,0,1,1),
    screen
)
scene.Camera.setCurrent(camera)
pygame.display.set_caption("RECUBE")
pygame.display.set_icon(pygame.image.load(setting.LOGO_PATH))
SCENE_MANAGER = scene.SceneManager(camera)
login_scene = go_login(lambda: go_home(pygame.Surface(setting.HOME_SIZE)))


#FramePool.run()
SCENE_MANAGER.RENDERING()
