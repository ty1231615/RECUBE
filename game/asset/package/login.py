import pygame
import datetime
import grpc
import asyncio
import os
import types
from typing import cast
import logging

from game.asset import scene,setting,conv,color,lang,animation,error
from game.asset.gui.object import circle,button
from game.cash import _Current_api,_User_account

from proto import account_pb2,account_pb2_grpc

logging.basicConfig(level=logging.INFO)

class LoginProof:
    def __init__(self,userName,UserPass,success_flag=None):
        self.__name = userName
        self.__pass = UserPass
        self.__invalid_time = None
        self.__account_channel = None
        self.__server_stub = None
        self.__validity = False
        self.__success_flag = success_flag
    @property
    def validity(self):
        return self.__validity
    @property
    def Channel(self):
        return self.__account_channel
    @property
    def invalid_time(self):
        return self.__invalid_time
    def Connection(self):
        self.__account_channel = grpc.insecure_channel(setting.ACCOUNT_NETWORK_ADDRESS)
        self.__server_stub = account_pb2_grpc.LoginAccountStub(self.Channel)
    async def ProofUpdate(self):
        while True:
            result = self.__server_stub.ContinuationSignal(account_pb2.ContinuationKey(key=_Current_api,id=_User_account.id),wait_for_ready=True)
            if not result:
                self.__validity = False
            print(f"CNT!{_Current_api}")
            await asyncio.sleep(150)
            if not self.__validity:
                return datetime.datetime.now()
    def AccountInit(self,account):
        global _User_account,_Current_api
        if account.state.LoginSCS:
            self.__validity = True
            _Current_api = account.apiKey
            self.__invalid_time = asyncio.get_event_loop().create_task(self.ProofUpdate())
            _User_account = account
            if self.__success_flag:
                self.__success_flag()
            logging.info("Account Validity!!")
    def singup(self) -> bool:
        CreateState = self.__server_stub.SingUp(account_pb2.LoginStatement(name=self.__name,password=self.__pass),wait_for_ready=True)
        self.AccountInit(CreateState.data)
    def login(self) -> bool:
        account = self.__server_stub.Login(account_pb2.LoginStatement(name=self.__name,password=self.__pass),wait_for_ready=True)
        print(account)
        self.AccountInit(account)


class LoginCanvas(scene.Scene):
    def __init__(self,next_button_padding=25,success_flag=None) -> None:
        super().__init__(pygame.Surface(setting.LOGIN_CANVAS_SIZE))
        self.__texts = lang.Texts()
        self.__success_flag = success_flag
        login_form = lang.Phrase("Login Form")
        login_form.add(
            lang.Lang(0,"アカウントにログイン"),
            lang.Lang(1,"Login Form")
        )
        input_name = lang.Phrase("Input Name")
        input_name.add(
            lang.Lang(0,"アカウント名を入力してください"),
            lang.Lang(1,"Input your account name")
        )
        input_password = lang.Phrase("Input Password")
        input_password.add(
            lang.Lang(0,"アカウントのパスワードを入力してください"),
            lang.Lang(1,"Input your account password")
        )
        next_button = lang.Phrase("NextButton")
        next_button.add(
            lang.Lang(0,"RECUBEにログイン"),
            lang.Lang(1,"Login to RECUBE")
        )
        signup_button = lang.Phrase("SignupButton")
        signup_button.add(
            lang.Lang(0,"アカウント作成"),
            lang.Lang(1,"Sign Up Account")
        )
        self.__texts.add(
            login_form,
            input_name,
            input_password,
            next_button,
            signup_button
        )
        center_x,center_y = self.get_center()
        mini_scale = 25
        self.__input_name_textbox = scene.TextBox(self.TEXT_TOP,conv.D2Position(center_x,center_y/1.5),lang.VariableFont(setting.DEFALT_FONT_PATH,lambda:self.get_size_average()/mini_scale),self.__texts.get(1).get_phrase(setting.LANG_NUMBER).value,text_color=color.COLOR(255,255,255))
        self.__input_password_textbox = scene.TextBox(self.TEXT_TOP,conv.D2Position(center_x,center_y/1.1),lang.VariableFont(setting.DEFALT_FONT_PATH,lambda:self.get_size_average()/mini_scale),self.__texts.get_phrase(2,setting.LANG_NUMBER).value,text_color=color.COLOR(255,255,255))
        self.TEXT_TOP.regit_text(self.__input_name_textbox)
        self.TEXT_TOP.regit_text(self.__input_password_textbox)
        self.__title_text = scene.TextView(self.__texts.get(0).get_phrase(setting.LANG_NUMBER).value,conv.D2Position(center_x,center_y/3),lang.VariableFont(setting.DEFALT_FONT_PATH,lambda: self.get_size_average()/mini_scale+5),0,color.COLOR(255,255,255))
        #self.circle = circle.Circle(self.surface,50)
        self.login_button = button.SimpleButton(conv.D2Position(center_x-next_button_padding*2,center_y+center_y/6),lang.VariableFont(setting.DEFALT_FONT_PATH,lambda:self.get_size_average()/mini_scale),0,self.__texts.get_phrase(3,setting.LANG_NUMBER).value,color.COLOR(0,0,0),color.COLOR(52, 235, 116),padding=next_button_padding,Click=lambda: self.__login_approach())
        self.signup_button = button.SimpleButton(conv.D2Position(center_x-next_button_padding*2,center_y+center_y/2),lang.VariableFont(setting.DEFALT_FONT_PATH,lambda:self.get_size_average()/mini_scale),0,self.__texts.get_phrase(4,setting.LANG_NUMBER).value,color.COLOR(0,0,0),color.COLOR(52, 235, 116),padding=next_button_padding,Click=lambda: self.__signup_approach())
        #self.camera_anim = animation.Animation(animation.Easing.ease_out_expl,animation.Easing.ease_in_expl,0,200,800,500)
    def __login_approach(self):
        proof = LoginProof(self.__input_name_textbox.texts,self.__input_password_textbox.texts,success_flag=self.__success_flag)
        proof.Connection()
        proof.login()
    def __signup_approach(self):
        proof = LoginProof(self.__input_name_textbox.texts,self.__input_password_textbox.texts,success_flag=self.__success_flag)
        proof.Connection()
        proof.singup()
    def setup(self, handler:scene.SceneManager):
        handler.resize(setting.LOGIN_CANVAS_SIZE)
    def render(self, surface:pygame.Surface):
        super().render()
        self.surface.fill(color.login_canvas_color())
        self.surface.blit(pygame.image.load(setting.BACKGROUND_IMAGE_PATH),(0,0))
        self.login_button.draw(self.surface)
        self.signup_button.draw(self.surface)
        self.TEXT_TOP.draw_texts(self)
        """
        ease = 0
        if self.camera_anim.finish:
            ease = self.camera_anim.back()
        else:
            ease = self.camera_anim.next()
        scene.Camera.CURRENT_RELATION.move_x = ease
        """
        self.surface.blit(*self.__title_text.view())
        surface.blit(self.surface,(scene.Camera._X(),scene.Camera._Y()))

class LoginScene(scene.Scene,scene.OnePage):
    def __init__(self,success_flag=None) -> None:
        super().__init__(pygame.Surface(setting.LOGIN_SIZE))
        super(scene.OnePage,self).__init__()
        self.add_page(LoginCanvas(success_flag=success_flag))
    def setup(self, handler:scene.SceneManager):
        handler.resize(setting.LOGIN_SIZE)
    def render(self,camera:scene.Camera):
        super().render()
        self.draw_page(camera.surface)