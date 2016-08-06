from kivy.app import App
from kivy.lang import  Builder
from kivy.uix.boxlayout import BoxLayout
class MBox(BoxLayout):
    pass
kv='''
<MBox>:
    Button:
        text:"<<Onceki"
        size_hint:1,.1
    Button:
        text:"Sonraki>>"
        size_hint:1,0.1
    BoxLayout:
        orientation:"vertical"
        pos_hint:{"right":1,"top":1}
        size_hint:3,1
        Label:
            text:"[anchor=title1][size=24]This is my Big [ref=w]title[/ref].[/size][anchor=content]Hello world"
            size_hint:1,0.1
            markup:True
            on_ref_press:print("www.google.com")

        GridLayout:
            size_hint:1,1
            cols:2
            padding:2
            spacing:2
            Image:
                source:"../images/images1.jpg"
            Image:
                source:"../images/images2.jpg"
            Image:
                source:"../images/images3.jpg"
            Image:
                source:"../images/images4.jpg"
            Image:
                source:"../images/images5.jpg"
            Image:
                source:"../images/images6.jpg"
            Image:
                source:"../images/images7.jpg"
            Image:
                source:"../images/images9.jpg"
'''
Builder.load_string(kv)
class LayoutDemo(App):
    def build(self):
        return MBox()
    def click(self,insta,val):
        print insta
        print val
if __name__ == '__main__':
    LayoutDemo().run()