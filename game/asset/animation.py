import types
from typing import Any

from game.asset import conv, scene

class Animation:
    def __init__(self,EasingFunction:types.MethodType,BackEasingFunction:types.MethodType,firstTime,from_value,to_value,duration) -> None:
        self._animator = EasingFunction
        self._back_animator = BackEasingFunction
        self._first_time = firstTime
        self.from_value = from_value
        self.to_value = to_value
        self.duration = duration
        self.finish = False
        self.progression = False
        self.init()
    def ease(self):
        return self._animator(self.progress,self.from_value,self.to_value,self.duration)
    def back_ease(self):
        return self._back_animator(self.progress,self.from_value,self.to_value,self.duration)
    def __call__(self, ease=None) -> Any:
        if ease:
            return ease(self.progress,self.from_value,self.to_value,self.duration)
        else:
            return self.ease()
    def next(self):
        if self.progress < self.duration:
            self.progress += 1
            self.progression = True
        if self.progress == self.duration:
            self.finish = True
            self.progression = False
        return self.ease()
    def back(self):
        if 0 < self.progress:
            self.progress -= 1
            self.progression = True
        if self.progress == 0:
            self.finish = False
            self.progression = False
        return self.back_ease()
    def init(self):
        self.progress = self._first_time
        self.finish = False
        self.progression = False

class Easing:
    @classmethod
    def ease_in_quad(cls,t, start_val, end_val, duration):
        progress = min(t / duration, 1.0)
        return start_val + (end_val - start_val) * progress**2
    @classmethod
    def ease_out_quad(cls,t, start_val, end_val, duration):
        progress = min(t / duration, 1.0)
        return start_val + (end_val - start_val) * (1 - (1 - progress)**2)
    @classmethod
    def ease_out_expl(cls,t,start_val,end_val,duration):
        progress = min(t / duration,1.0)
        return start_val + (end_val - start_val) * (1 - pow(2,-10 * progress))
    @classmethod
    def ease_in_expl(cls,t,start_val,end_val,duration):
        progress = min(t / duration,1.0)
        return start_val + (end_val - start_val) * pow(2,10 * progress - 10)