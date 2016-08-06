#:-*- coding:utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
kv='''
<MPopup>:
    size_hint:0.7,0.2
    title:"UmutRss Feeder Mesaj"
    BoxLayout:
        orientation:"vertical"
        Label:
            id:lbl
            text:root.lbl
        Button:
            text:"Tamam"
            on_press:root.dismiss()
<TextInput>:
    font_name:"ubu"
<MiButton>:
    font_name:"ubu"
<PanelScreen>:
    name:"panelscreen"
    urladres:urladres
    drp:drp
    haberadi:haberadi
    takmaadi:takmaadi
    ScrollView:
        BoxLayout:
            orientation:"vertical"
            padding:5
            spacing:2
            size_hint_y:None
            height:dp(1000)
            Button:
                size_hint:None,None
                size:50,50
                text:"[font=ifont]<[/font]"
                markup:True
                pos_hint:{"right":1}
                on_release:root.manager.current="homescreen"
            Label:
                text:"UmutRss Feeder Feed Ekleme"
            Label:
                text:"Haber Site Adı"
            TextInput:
                id:haberadi
                hint_text:"site adi giriniz"
            Label:
                text:"Haber site takma adı"
            TextInput:
                id:takmaadi
                hint_text:"site takma adinda turkce karakter kullanmayiniz"
            Label:
                text:"Kategori"
            Button:
                id:drp
                text:"Kategori Seç"
            Label:
                text:"url adresi"
            TextInput:
                id:urladres
            Button:
                text:"Tamam"
                on_press:root.setValues()


'''
Builder.load_string(kv)
class MiButton(Button):
    key=StringProperty()
class MPopup(Popup):
    lbl=StringProperty()
    def __init__(self,title,**k):
        super(MPopup,self).__init__(**k)
        self.lbl=title
class PanelScreen(Screen):
    def on_enter(self, *args):
        super(PanelScreen,self).on_enter(*args)
        self.entered=True
        self.selectedCat=None
        js=JsonStore("titles.json")
        titles=js.get("titles")
        drop=DropDown()
        for t in titles["all"]:
            btn=MiButton(text=titles["all"][t],size_hint_y=None,height=50,key=t)
            btn.bind(on_release=lambda btn:drop.select(btn))
            drop.add_widget(btn)
        def set_select(inst,btn):
            self.drp.text=btn.text
            self.selectedCat=btn.key
        drop.bind(on_select=set_select)
        self.drp.bind(on_release=drop.open)
    def setValues(self):
        cat=self.selectedCat
        url=self.urladres.text
        if len(self.haberadi.text)>3 and len(self.takmaadi.text)>3 and len(cat)>3 and len(url)>3:
            if self.entered:
                self.entered=False
                self.haberadi.disabled=True
                self.takmaadi.disabled=True
                self.urls = dict()
            self.urls[cat]=url
            MPopup(title=u"Başarıyla Eklendi").open()
        else:
            MPopup(title=u"Tüm alanları doldurunuz").open()
    def on_pre_leave(self, *args):
        if len(self.haberadi.text)<3 and len(self.takmaadi.text)<3:
            return
        js=JsonStore("UmutRss.json")
        fst=True
        url_str="{"
        for k,v in self.urls.items():
            if fst:
                url_str +=k+":"+v
                fst=False
            else:
                url_str += ","+k + ":" + v

        url_str +="}"
        js.put(self.haberadi.text,title=self.takmaadi.text,url=url_str)
