#-*- coding:utf-8 -*-
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
kv='''
<BoxLayout>:
    Button:
        text:"Çal"
        on_release:app.cal()
    Button:
        text:"Duraklat"
        on_press:app.duraklat()
    Button:
        text:"Durdur"
        on_press:app.durdur()
    Button:
        text:"Sürekli Çal"
        on_press:app.surekli()




'''

class soundApp(App):
    def build(self):
        return BoxLayout()
    def cal(self):
        if hasattr(self,"sound") and hasattr(self,"sndpos"):
            self.sound.play()
            self.sound.seek(self.sndpos)
            return
        self.sound=SoundLoader.load("bagdat.mp3")
        self.sound.play()
    def duraklat(self):
        if self.sound:
            self.sndpos=self.sound.get_pos()
            self.sound.stop()
    def durdur(self):
        if self.sound:
            self.sound.stop()
            self.sndpos=0
    def surekli(self):
        if self.sound:
            self.sound.loop=True
if __name__ == '__main__':
    Builder.load_string(kv)
    soundApp().run()