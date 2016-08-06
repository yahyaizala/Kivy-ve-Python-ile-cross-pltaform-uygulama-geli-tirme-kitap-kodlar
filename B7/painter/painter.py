from kivy.app import runTouchApp,App
from kivy.graphics import Color,Rectangle,Mesh
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.core.window import Window
kv='''
<MRelativeLayout>:
    id:rlt
    canvas:
        Color:
            rgb:1,0,0
        Rectangle:
            size:100,100
            pos:100,100
        Color:
            rgba:0,1,0,1
        Line:
            width:1
            rectangle:202,100,100,100
        Color:
            rgb:0,0,1
        Line:
            bezier:300,300,300,100,400,50
        Color:
            rgb:0.2,0.2,0.2
        Line:
            circle:400,125,50
        Line:
            circle:100,300,50,-45,225
    MButton:
        root:rlt
        size_hint:None,None
        size:50,30
        pos:root.width/2,root.height/2
        text:"yahya"





'''
class MButton(Button):
    def __init__(self,**k):
        super(self.__class__,self).__init__(**k)
        with self.canvas:
            Color(1, 0, 1)
            self.rect=Rectangle(size=(50,30),pos=(Window.width/2.0,Window.height/2.0))
        self.bind(pos=self.updte)
        self.bind(size=self.updte)
    def updte(self,*args):
        self.rect.pos=self.pos
        self.rect.size=self.size

class MRelativeLayout(RelativeLayout):
    def __init__(self,**k):
        super(self.__class__,self).__init__(**k)
        self.rect=None
        self.graph=None
    def on_touch_down(self, touch):
        self.rect=True
        self.xi,self.yi=touch.pos
        with self.canvas:
            Color(1,0,0)
            self.rect=Rectangle(pos=(self.xi,self.yi),size=(1,1))
    def on_touch_move(self, touch):
        if self.rect:
            ix,iy=(touch.x-self.xi),(touch.y-self.yi)
            self.canvas.remove(self.rect)
            self.rect=Rectangle(pos=(self.xi,self.yi),size=(ix,iy))
            self.canvas.add(self.rect)
    def on_touch_up(self, touch):
        if self.rect:
            ix, iy = (touch.x - self.xi), (touch.y - self.yi)
            self.canvas.remove(self.rect)
            self.rect = Rectangle(pos=(self.xi, self.yi), size=(ix, iy))
            self.canvas.add(self.rect)



Builder.load_string(kv)
runTouchApp(MRelativeLayout())