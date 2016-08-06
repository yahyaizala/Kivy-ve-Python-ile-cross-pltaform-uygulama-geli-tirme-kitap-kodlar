from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty,StringProperty
from kivy.uix.popup import Popup
from plyer import vibrator
from plyer import accelerometer
from kivy.core.audio import SoundLoader

class Evil(Widget):
    pass
class MPop(Popup):
    lbl=StringProperty()
class MyWidget(Widget):
    pass
class Player(Widget):
    def move(self,x,y):
        self.x -=x
        self.y -=y
    @staticmethod
    def error(text="NotImplementedError Hatasi"):
        p = MPop()
        p.lbl = text
        p.open()
    @staticmethod
    def yandin():
        p = MPop()
        p.title="Canin Gitti Ekrani"
        p.lbl = "Yandin!"
        p.open()
class Background(RelativeLayout):
    player=ObjectProperty()
    evil=ObjectProperty()
    def __init__(self,**kwargs):
        super(Background,self).__init__(**kwargs)
        self.start_game()
        self.play_audio(fname="lops.wav")
    def play_audio(self,fname):
        SoundLoader.load(fname).play()
    def start_game(self):
        self.setChilds()
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.move,20**-1)
        except NotImplementedError:
            Player.error()
    def move(self,dt):
        for child in self.others:
            if child.collide_point(self.player.x,self.player.y):
                Player.yandin()
        vec=accelerometer.acceleration[:2]
        if not vec==(None,None):
            self.player.move(vec[0],vec[1])
        if self.player.collide_point(self.evil.x,self.evil.y):
            if vibrator:
                vibrator.vibrate(10)
            else:
                Player.error(text="plyer vibrate")
    def setChilds(self):
        self.others = []
        for child in self.children:
            if not isinstance(child,Player) and not isinstance(child,Evil):
                self.others.append(child)



class canvarApp(App):
    def build(self):
        return Background()
if __name__ == '__main__':
    canvarApp().run()