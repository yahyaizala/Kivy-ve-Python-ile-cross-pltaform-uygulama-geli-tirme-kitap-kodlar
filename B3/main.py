#-*- coding:utf-8 -*-
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView
from kivy.animation import Animation,AnimationTransition
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.video import Video
import os
class MVideo(Video):
    pass
class About(ModalView):
    def __init__(self,**kwargs):
        super(About,self).__init__(**kwargs)
        Clock.schedule_once(self.dismiss_pop,2)
    def dismiss_pop(self,dt):
        self.dismiss()
class MButton(ToggleButton):
    name=""
    index=-1
class FileOpen(ModalView):
    pass
class PlayerItems(object):
    filename=""
    filepath=""
    isDown=False
    def __init__(self,**kwargs):
        self.filename=kwargs.get("filename")
        self.filepath=kwargs.get("filepath")
class VolumeSlider(ModalView):
    def __init__(self,video,**kwargs):
        super(VolumeSlider,self).__init__(**kwargs)
        self.vid=video
        self.vSlider.bind(value=self.setVideoVol)
    def setVideoVol(self,ins,val):
        self.vid.volume=val
class PlayerList(ModalView):
    pass
class KVideoplayer(RelativeLayout):
    video=ObjectProperty()
    thumb=ObjectProperty()
    controls=ObjectProperty()
    showing=True
    playerList=[]
    def load(self,path,file):
        for f in file:
            pit=PlayerItems()
            pit.filename=f
            pit.filepath=f
            pit.isDown=False
            if pit not in self.playerList:
                self.playerList.append(pit)

        self.video.source=self.playerList[0].filepath
        self.fileOpens.dismiss()

    def openFileChooser(self):
        self.fileOpens=FileOpen()
        self.fileOpens.open()
        self.fileOpens.fc.bind(on_submit=self.load_by_touch)
    def load_by_touch(self,ins,path,touch):
        try:
            self.load(path,ins.selection)
        except:
            self.fileOpens.dismiss()
    def volumeOpen(self):
        vol=VolumeSlider(self.video)
        vol.vSlider.value=self.video.volume
        anim=Animation(duration=.5,t=AnimationTransition.in_out_bounce,x=self.width-vol.width)
        anim.start(vol)
        vol.open()

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.videoPlayPause()
        if self.vProg.collide_point(*touch.pos):
            self.vprev=self.video.state
            self.vtouch=touch
            self.video.unbind(position=self.posListen)
        self.touch_controls()
        super(KVideoplayer,self).on_touch_down(touch)
    def on_touch_up(self, touch):
        if self.vProg.collide_point(*touch.pos) and hasattr(self,"vprev") and touch is self.vtouch:
            self.video.seek(self.vProg.value)
            self.thumb.opacity=0
            if self.video.state!="stop":
                self.video.state=self.vprev
                self.video.bind(position=self.posListen)
            return
        vec=Vector(touch.pos)-Vector(touch.opos)
        if vec.length()<10:
            return
        if abs(vec.x)<abs(vec.y):
            about=About()
            about.open()
            return
        if abs(vec.x)>abs(vec.y):
            if vec.x<0:
                self.openFileChooser()
            if  vec.x>0:
                self.openPlayerList()
        super(KVideoplayer,self).on_touch_up(touch)
    def openPlayerList(self):
        if not hasattr(self,"plyerList"):
            self.plyerList=PlayerList()
        else:
            self.plyerList.container.clear_widgets()
        if len(self.playerList)>0:
            for itm in self.playerList:
                finame=os.path.basename(itm.filepath)
                btn = MButton(size_hint=(1, None), text=finame[:-4],
                             height=50,group="plyer")
                btn.name =itm.filepath
                if itm.isDown:
                    btn.state="down"
                index=self.playerList.index(itm)
                btn.index=index
                btn.bind(on_release=self.open_music)
                self.plyerList.container.add_widget(btn)
            self.plyerList.open()
            height = len(self.plyerList.container.children) * 50
            self.plyerList.container.height = height

    def open_music(self,instance):
        self.video.source=instance.name
        instance.state="down"
        for p in self.playerList:
            p.isDown=False
        self.playerList[instance.index].isDown=True
        self.plyerList.dismiss()
        self.playVideo()
    def playVideo(self):
        self.video.state="play"
        self.thumb.opacity=0
    def videoPlayPause(self):
        if self.video.state == "play":
            self.video.state = "pause"
            self.thumb.opacity = 1
        elif self.video.state == "stop" or self.video.state == "pause":
            self.video.state = "play"
            self.thumb.opacity = 0
            for p in self.playerList:
                if p.filepath==self.video.source:
                    p.isDown=True
                    break
    def stopVideo(self):
        if self.video.state=="play" or self.video.state=="pause":
            self.video.state="stop"
            self.thumb.opacity=1
            self.vProg.value=0
    def __init__(self,**kwargs):
        super(KVideoplayer,self).__init__(**kwargs)
        self.video.bind(state=self.stateListen)
        self.video.bind(position=self.posListen)
        self.video.bind(eos=self.next)
    def next(self,instance,val):
        if self.playerList.__len__()>0:
            curIndex=-1
            for p in self.playerList:
                if p.isDown:
                    curIndex=self.playerList.index(p)
                    break
            if curIndex>-1:
                curIndex+=1
                if curIndex<len(self.playerList):
                    for p in self.playerList:
                        p.isDown=False
                    self.video.source=self.playerList[curIndex].filepath
                    self.playerList[curIndex].isDown=True
                    self.playVideo()
    def stateListen(self,ins,val):
        if val=="play":
            self.ply.background_normal = "ps_nrml.png"
            self.ply.background_down = "ps_down.png"
            if self.showing :
                self.hideControls()
        elif val=="pause" or val=="stop":
            self.ply.background_normal = "ply_nrm.png"
            self.ply.background_down = "ply_down.png"
            self.showControls()
    def hideControls(self):
        anim=Animation(y=-self.controls.height-10,d=2,t=AnimationTransition().in_out_quint)
        anim.start(self.controls)
        anim.bind(on_complete=self.setShow)
    def setShow(self,ins,val):
        self.showing=not self.showing
        print self.showing
    def showControls(self,callback=False):
        if not self.showing:
            anim = Animation(t=AnimationTransition().in_back, d=1, y=self.controls.height / 2.0 - 5)
            anim.start(self.controls)
            anim.bind(on_complete=self.setShow)
    def touch_controls(self):
        if not self.showing:
            anim=Animation(t=AnimationTransition().in_expo,y=self.controls.height/2.0-5)
            anim.bind(on_complete=self.setHide)
            anim.start(self.controls)

    def setHide(self,ins,val):
        def hide(dt):
            if not self.showing:
                anim = Animation(t=AnimationTransition.in_sine, y=-self.controls.height - 10, d=1.5)
                anim.start(self.controls)
        Clock.schedule_once(hide,5)
    def posListen(self,ins,val):
        progression=float(val)/float(ins.duration)
        self.vProg.value=progression
        min,sec=divmod(ins.duration,60)
        timepass=val
        tmin,tsec=divmod(timepass,60)
        self.vLabel.text="%.2i:%.2i/%.2i:%.2i"%(int(tmin),int(tsec),int(min),int(sec))
class VideoApp(App):
    def build(self):
        return KVideoplayer()
if __name__ == '__main__':
    LabelBase.register(name="ubu",fn_regular="UbuntuMono.ttf")
    Window.clearcolor = (.2, .2, 0.2, 1)
    VideoApp().run()