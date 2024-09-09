import types

def ease_23_in(time,begin,change,duration):
    return -change * (( time / duration - 1)**4- 1) + begin

class Easing:
    def __init__(self,begin,last,addTime=1,duration=1000) -> None:
        self.__begin = begin
        self.__last = last
        self.__addtime = addTime
        self.__duration = duration
        self.__time_progress = 0
        self.__finish = False
    def set_progress(self,time):
        self.__time_progress = time
    def update(self):
        self.__time_progress+=self.addTime
        if self.__time_progress >= self.duration:
            self.__time_progress = self.duration
            self.__finish = True
    def reset(self):
        self.__time_progress = 0
        self.__finish = False
    @property
    def finish(self):
        return self.__finish
    @property
    def progress(self):
        return self.__time_progress
    @property
    def begin(self):
        return self.__begin
    @property
    def last(self):
        return self.__last
    @property
    def addTime(self):
        return self.__addtime
    @property
    def duration(self):
        return self.__duration

class Ease23(Easing):
    def update(self):
        super().update()
        return ease_23_in(self.progress,self.begin,self.last,self.duration)

