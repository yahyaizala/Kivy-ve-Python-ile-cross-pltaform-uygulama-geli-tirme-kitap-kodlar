#-*- coding:utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import  RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.vector import Vector
from kivy.animation import Animation,AnimationTransition
import xml.etree.ElementTree as ET
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty,StringProperty
import time
import re
import webbrowser
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
Builder.load_file("home.kv")
class MBox(BoxLayout):
    title=StringProperty()
    description=StringProperty()
    img=StringProperty()
    clickable=ObjectProperty()
class MLabel(Label):
    pass
class ClickableLabel(ButtonBehavior,MLabel):
    url=StringProperty()
    def __init__(self,**kwargs):
        super(ClickableLabel,self).__init__(**kwargs)
    def on_press(self):
        try:
            webbrowser.open(url=self.url)
        except:
            from jnius import autoclass,cast
            Context=autoclass("org.renpy.PythonActivity").mActivity
            Uri=autoclass("android.net.Uri")
            Intent=autoclass("android.content.Intent")
            intent=Intent()
            intent.setAction(Intent.ACTION_VIEW)
            curIntent=cast("android.app.Activity",Context)
            curIntent.startActivity(intent)


class MToggleButton(ToggleButton):
    urlToShow=""
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    @staticmethod
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def on_press(self):
        self.reqData()
    def reqData(self):
        url=self.urlToShow
        UrlRequest(req_headers=self.headers,method="GET",url=url,on_success=self.gotData,on_error=self.error)
    def gotData(self,req,data):
        datas=ET.fromstring(data.encode("utf-8"))
        if len(self.ac.children):
            self.ac.clear_widgets()
        self.ac.bind(minimum_height=self.ac.setter("height"))
        #rot=datas[0][0]
        #print rot.text
        for item in datas.iter("item"):
            title=item.find("title").text
            summary=item.find("description").text
            pubDate=item.find("pubDate").text
            format="%a, %d %b %Y %H:%M:%S %Z"
            strpide=time.strptime(pubDate,format)
            localize=time.localtime(time.mktime(strpide))
            pubDate=time.strftime("%d/%m/%Y %H:%M:%S",localize)
            try:
                img=item.find("enclosure").attrib["url"]
            except:
                img="yok.jpg"
            mb=MBox()
            mb.title=title
            summary=self.cleanhtml(summary)
            st=u"Devami için tıklayınız"
            fnd=u"için tıkla"
            if fnd in summary:
                summary=summary[:-len(st)]
            summary=summary+"\t\t[b][color=#abcabc]"+str(pubDate)+"[/color][/b]"
            mb.description=self.cleanhtml(summary)
            mb.img=img
            link=item.find("link").text
            mb.clickable.url=link
            self.ac.add_widget(mb)
        self.gndmLabel.text=HomeScreen.title+"-"+self.text
    def error(self,req,data):
        print data


class LeftSide(RelativeLayout):
    pass
class HomeScreen(Screen):
    urls=[]
    title=""
    container=ObjectProperty()
    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        vec=Vector(touch.pos)-Vector(touch.opos)
        if vec.length()>10:
            if abs(vec.x)>abs(vec.y):
                if vec.x>0:
                    self.fadeMenu()
    def fadeMenu(self):
        try:
            Clock.unschedule(self.startUnfader)
        except:
            pass
        anim=Animation(x=0,t=AnimationTransition.out_expo,duration=.9)
        anim.bind(on_complete=self.unfadeMenu)
        anim.start(self.side)
    def unfadeMenu(self,anim,val):
        Clock.schedule_once(self.startUnfader,3.5)
    def startUnfader(self,dt):
        targetX=-self.side.width-self.manager.width*0.2
        anim=Animation(x=targetX,t=AnimationTransition.in_out_sine,d=.5)
        anim.start(self.side)
    def on_enter(self, *args):
        self.setUrls()
    def addNews(self,widget):
        self.container.add_widget(widget)
    def setUrls(self):
        if self.urls.__len__()>0:
            if hasattr(self,"side"):
                self.side.container.clear_widgets()
                self.remove_widget(self.side)
                del self.side
            title=JsonStore("titles.json")
            titles=title.get("titles")
            self.side = LeftSide()
            for k in self.urls:
                all=titles["all"]
                if all[k]:
                    lbl = MToggleButton(text=all[k], size_hint=(1, None), height=100)
                    lbl.urlToShow = self.urls[k]
                    lbl.ac=self.container
                    lbl.gndmLabel=self.gndmLabel
                    if all[k]==u"Gündem":
                        lbl.state="down"
                        self.gndmLabel.text=self.title+u" Gündem"
                        lbl.reqData()
                    self.side.container.add_widget(lbl)
            self.add_widget(self.side)
            self.side.x=-self.side.width-self.manager.width*0.2
            self.side.y=0
            self.side.container.height=100*(len(self.side.container.children))
