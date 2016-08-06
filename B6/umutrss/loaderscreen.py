from kivy.uix.screenmanager import Screen
from kivy.animation import Animation,AnimationTransition
class LoaderScreen(Screen):
    def on_pre_enter(self, *args):
        self.opacity=0
    def on_enter(self, *args):
        anim = Animation(opacity=1, d=1.5, t=AnimationTransition.in_sine)
        anim.bind(on_complete=self.toggle)
        anim.start(self)
    def toggle(self,anim,dt):
        anim=Animation(opacity=0,d=1.5,t=AnimationTransition.out_sine)
        anim.bind(on_complete=self.go_next)
        anim.start(self)
    def go_next(self,anim,dt):
        self.manager.current="mainscreen"
