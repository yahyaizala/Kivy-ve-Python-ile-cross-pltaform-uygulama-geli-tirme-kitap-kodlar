from kivy.config import Config
Config.set("graphics","width","450")
Config.set("graphics","height","600")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,SlideTransition
from index import MainScreen
from home import HomeScreen
from kivy.core.window import Window
from addpanel import *
from kivy.core.text import LabelBase
Builder.load_file("loaderscreen.kv")
class UmutRssManager(ScreenManager):
    pass
class UmutrssApp(App):
    use_kivy_settings = False
    def build(self):
        self.root=UmutRssManager(transition=SlideTransition())
        Window.bind(on_keyboard=self.hook_kb)
        return self.root
    def hook_kb(self, win, key, *largs):
        if key == 27:
            if self.root:
                prev = self.root.previous()
                self.root.current = prev
            return True
        return False

if __name__ == '__main__':
    LabelBase.register(name="ubu",fn_regular="ubuntu.ttf")
    LabelBase.register(name="ifont",fn_regular="Byom-Icons-Trial.ttf")
    UmutrssApp().run()