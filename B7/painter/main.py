from kivy.app import runTouchApp
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color,Rectangle,Line,Ellipse,Bezier
from kivy.uix.scatter import Scatter
from kivy.uix.modalview import ModalView
from  kivy.uix.stencilview import StencilView
gui='''
<MModal>:
    cp:cp
    size_hint:0.5,0.5
    BoxLayout:
        pos_hint:{"center_x":0.5,"center_y":0.5}
        ColorPicker:
            id:cp
<ToggleButton>:
    size_hint:None,None
    size:60,60
    background_color:1,1,1,1
<Button>:
    size_hint:None,None
    size:60,60
#:import clr kivy.utils.get_color_from_hex
<MRelativeLayout>:
    mycanvas:mycanvas
    clrbtn:btn
    AnchorLayout:
        anchor_x:"left"
        anchor_y:"top"
        BoxLayout:
            size_hint:None,None
            orientation:"vertical"
            width:60
            height:300
            Button:
                id:btn
                background_color:clr("db981b")
                on_release:root.open_picker()
            ToggleButton:
                group:"point"
                on_release:mycanvas.set_width(1)
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        x:self.x
                        y:self.y
                    Point:
                        points:30,30
                        pointsize:1
                    PopMatrix

            ToggleButton:
                group:"point"
                on_release:mycanvas.set_width(3)
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Point:
                        points:30,30
                        pointsize:3
                    PopMatrix

            ToggleButton:
                group:"point"
                on_release:mycanvas.set_width(5)
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Point:
                        points:30,30
                        pointsize:5
                    PopMatrix
            ToggleButton:
                group:"point"
                on_release:mycanvas.set_width(7)
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Point:
                        points:30,30
                        pointsize:7

                    PopMatrix
    AnchorLayout:
        anchor_x:"right"
        anchor_y:"top"
        BoxLayout:
            orientation:"vertical"
            size_hint:None,None
            width:60
            height:300
            ToggleButton:
                group:"shape"
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Line:
                        points:10,10,50,50
                    PopMatrix
                on_release:mycanvas.set_which("line")

            ToggleButton:
                group:"shape"
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Line:
                        circle:30,30,15
                    PopMatrix
                on_release:mycanvas.set_which("circle")
            ToggleButton:
                group:"shape"
                canvas.after:
                    PushMatrix
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Line:
                        rectangle:10,10,40,40
                    PopMatrix
                on_release:mycanvas.set_which("rectangle")
            ToggleButton:
                group:"shape"
                canvas.after:
                    PushMatrix:
                    Color:
                        rgb:clr("#0f1111")
                    Translate:
                        xy:self.pos
                    Line:
                        bezier:5,5,30,20,10,10,30,50,40,5
                        dash_length:5
                    PopMatrix
                on_release:mycanvas.set_which("free")
            Button:
                text:"[color=e1f4e3]Sil[/color]"
                background_color:clr("c56646")
                markup:True
                on_press:mycanvas.clear()

    AnchorLayout:
        anchor_x:"center"
        anchor_y:"center"
        MStencilView:
            id:mycanvas
            size_hint:None,None
            width:root.width-130
            height:root.height-10
            canvas:
                Color:
                    rgb:(.2,.2,.2)
                Rectangle:
                    pos:self.pos
                    size:self.size





'''
Builder.load_string(gui)
class Painter(object):
    mcolor=get_color_from_hex("db981b")
    width=1
    @staticmethod
    def draw_rect(x,y,w,h):
        return Rectangle(pos=(x,y),size=(w,h),width=Painter.width)
    @staticmethod
    def draw_line(x1,y1,x2,y2):
        return Line(points=(x1,y1,x2,y2),width=Painter.width)
    @staticmethod
    def draw_circle(x,y,r):
        return Line(circle=(x,y,r),width=Painter.width)


class MModal(ModalView):
    pass
class MStencilView(StencilView):
    selected=None
    which=""
    def clear(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.2,0.2,0.2)
            Rectangle(pos=(self.x,self.y),size=(self.width,self.height))
    def set_which(self,whc):
        self.which=whc
    def set_width(self,val):
        Painter.width=float(val)
    def set_draw(self,touch):
        w,h=touch.x-self.ix,touch.y-self.iy
        if self.which=="rectangle":
            self.selected=Painter.draw_rect(self.ix,self.iy,w,h)
        elif self.which=="line":
            self.selected=Painter.draw_line(self.ix,self.iy,touch.x,touch.y)
        elif self.which=="circle":
            import math
            r=math.hypot(w,h)
            self.selected=Painter.draw_circle(self.ix,self.iy,r)


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.ix=touch.x;self.iy=touch.y
            with self.canvas:
                Color(*Painter.mcolor)
                if self.which=="free":
                    touch.ud["line"]=Line(points=(self.ix,self.iy),width=Painter.width)
                    if self.selected:
                        self.selected=None
                else:
                    self.set_draw(touch)
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and self.selected:
            w,h=touch.x-self.ix,touch.y-self.iy
            self.canvas.remove(self.selected)
            with self.canvas:
                    self.set_draw(touch)
        if self.collide_point(*touch.pos) and self.which=="free":
            touch.ud["line"].points += [touch.x, touch.y]



    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.selected:
            w,h=touch.x-self.ix,touch.y-self.iy
            self.canvas.remove(self.selected)
            with self.canvas:
                self.set_draw(touch)

        super(MStencilView,self).on_touch_down(touch=touch)
class MRelativeLayout(RelativeLayout):
    def open_picker(self):
        m=MModal()
        m.cp.bind(color=self.color_select)
        m.open()
    def color_select(self,picker,val):
        Painter.mcolor=val
        self.clrbtn.background_color=Painter.mcolor

runTouchApp(MRelativeLayout())