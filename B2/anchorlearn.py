from kivy.app import runTouchApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
kv=Builder.load_string('''
#:import clr kivy.utils.get_color_from_hex
<Button>:
    font_name:"ifont"
    font_size:50
    background_color:clr("#d85858")
    size_hint:None,None
    height:120
    width:50
<FButton@Button>:
    size_hint:1,None
    height:50
AnchorLayout:
    spacing:5
    spacing:5
    AnchorLayout:
        anchor_x:"right"
        anchor_y:"top"
        BoxLayout:
            orientation:"vertical"
            size_hint:.1,.8
            pos_hint:{"top":1}
            Button:
                text:"`"
            Button:
                text:"D"
            Button:
                text:"E"
            Button:
                text:"i"
    AnchorLayout:
        anchor_x:"left"
        acnhor_y:"top"
        AsyncImage:
            size_hint:0.9,.8
            id:_img
            source:"rotational.jpg"
    AnchorLayout:
        anchor_x:"center"
        anchor_y:"bottom"
        BoxLayout:
            size_hint:.1,0.1
            FButton:
                text:"H"
            FButton:
                text:"G"
''')
if __name__ == '__main__':
    LabelBase.register(name="ifont",fn_regular="PWSmallIcons.ttf")
    runTouchApp(kv)