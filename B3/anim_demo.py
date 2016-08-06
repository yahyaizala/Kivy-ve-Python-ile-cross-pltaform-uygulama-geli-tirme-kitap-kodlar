#-*- coding:utf-8 -*-
from kivy.app import App
from kivy.animation import Animation,AnimationTransition
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
kv='''
<Button>:
    size_hint:None,None
    height:50
    width:150
<MWin>:
    obje:obje
    AnchorLayout:
        anchor_x:"left"
        anchor_y:"top"
        Accordion:
            orientation:"vertical"
            size_hint:None,.4
            width:150
            collapse:True
            AccordionItem:
                title:"Ard Arda Animasyon"
                Button:
                    text:"Hareket Ettir"
                    on_press:app.squenceAnim()
                    background_color:(1,0.7,0.9,1)


            AccordionItem:
                title:"Paralel Animasyon"
                Button:
                    text:"Animate"
                    on_press:app.paralelAnim()
                    background_color:(1,0.7,0.9,1)
            AccordionItem:
                title:"Normal Animasyon"
                BoxLayout:
                    orientation:"vertical"
                    Button:
                        text:"Kaybet/Göster"
                        on_release:app.hideAnim()
                        background_color:(1,0.7,0.9,1)
                    Button:
                        text:"Büyüt/Küçült"
                        on_press:app.bigAnim()
                        background_color:(1,0.7,0.9,1)
    Image:
        id:obje
        pos:200,200
        source:"angry-bird-icon.png"
        size_hint:None,None
        size:100,100





'''
class MWin(RelativeLayout):
    pass
class animApp(App):
    def build(self):
        return MWin()

    def loopAnim(self):
        anim = Animation(d=2, t="in_back", size=(50, 50))+Animation(d=1,t="in_back",pos=(400,400))
        #anim.repeat = True
        anim.start(self.root.obje)
    def squenceAnim(self):
        X=self.root.obje.x
        w,h=self.root.obje.width,self.root.obje.height
        anim=Animation(duration=2,size=(100,100),transition=AnimationTransition().in_out_expo)
        anim +=Animation(x=self.root_window.width)
        anim +=Animation(x=X)
        anim +=Animation(size=(w,h))
        anim.start(self.root.obje)
    def paralelAnim(self):
        anim = Animation(duration=2, transition=AnimationTransition().in_out_expo, y=self.root_window.height-100)
        anim &= Animation(size=(50, 50))
        anim &=Animation(x=300)
        anim.start(self.root.obje)

    def bigAnim(self,ins=None,val=None):
        anim=Animation(d=3,t="in_out_sine",size=(300,300))
        anim.start(self.root.obje)
        anim.bind(on_complete=self.litAnim)
    def litAnim(self,ins,val):
        anim=Animation(d=3,t=AnimationTransition().in_elastic,size=(150,50))
        anim.bind(on_complete=self.bigAnim)
        anim.start(self.root.obje)

    def hideAnim(self):
        anim=Animation(opacity=0,d=3,t="in_out_bounce")
        anim.start(self.root.obje)
        anim.bind(on_complete=self.show)
    def show(self,ins,val):
        anm=Animation(opacity=1,t=AnimationTransition().in_out_expo)
        anm.start(self.root.obje)
if __name__ == '__main__':
    Builder.load_string(kv)
    animApp().run()
