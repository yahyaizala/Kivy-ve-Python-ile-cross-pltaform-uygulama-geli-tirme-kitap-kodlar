from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import get_color_from_hex as clr
from kivy.graphics import Color,Line
class MyWidget(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*clr("#abcabc"))
                self.rect=Line(rectangle=(self.x,self.y,self.width,self.height),dash_offset=3)
                return super(MyWidget,self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(touch.x,touch.y) and self.rect:
            self.center_x,self.center_y=touch.pos
            self.canvas.remove(self.rect)
            with self.canvas:
                self.rect=Line(rectangle=(self.x,self.y,self.width,self.height),dash_offset=3)
            return True
        return super(MyWidget,self).on_touch_down(touch)
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.canvas.remove(self.rect)

kv='''
<RelativeLayout>:
    size_hint:1,1
    MyWidget:
        size_hint:None,None
        size:50,50
        canvas:
            Rectangle:
                source:"baloon.jpg"
                size:self.size
                pos:self.pos

'''
Builder.load_string(kv)
class WidgetApp(App):
    def build(self):
        return RelativeLayout()
if __name__ == '__main__':
    WidgetApp().run()