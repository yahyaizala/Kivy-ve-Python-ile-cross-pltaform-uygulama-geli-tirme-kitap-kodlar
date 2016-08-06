#-*- coding:utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.modalview import ModalView
from kivy.animation import AnimationTransition,Animation
from kivy.core.audio import SoundLoader
from random import randrange
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import NumericProperty,StringProperty
from kivy.animation import AnimationTransition,Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
import json
from kivy.network.urlrequest import UrlRequest
from urllib import urlencode
from kivy.core.window import Window
import sqlite3
class EndPanel(ModalView):
    def exit(self):
        self.dismiss()
        cPanel=CikisPanel()
        cPanel.open()
        app = KgameApp.get_running_app()
        root = app.root
        cPanel.x = root.width + cPanel.width
        cPanel.bind(on_dismiss=self.dist)
        anim = Animation(d=1, t=AnimationTransition.out_sine, center_x=root.center_x, center_y=root.center_y)
        anim.start(cPanel)
    def dist(self,inst):
        app=KgameApp.get_running_app()
        app.root.get_screen("game").reset()
    def newGame(self):
        self.dismiss()
        app=KgameApp.get_running_app()
        sm=app.root
        curScreen=sm.get_screen("game")
        curScreen.reset()

class ErrPanel(ModalView):
    pass
class AboutPanel(ModalView):
    pass
class SesPanel(ModalView):
    pass
class MScreenManager(ScreenManager):
    pass
class ImageButton(ButtonBehavior,Image):
    num=NumericProperty()
    def __init__(self,num,**kwargs):
        super(ImageButton,self).__init__(**kwargs)
        self.num=num
class SScreen(Screen):
    def on_enter(self, *args):
        KgameApp.load("sounds/level1.ogg")
    def on_pre_leave(self, *args):
        KgameApp.looper.stop()
class GScreen(Screen):
    imageArray=[]
    flipedImages=[]
    finedImages=[]
    objects=[]
    clickable=True
    timer=300
    ticks=-1
    puan=0
    mytime=-1
    gameOver=False
    def reset(self):
        self.imageArray = []
        self.flipedImages = []
        self.finedImages = []
        self.objects = []
        self.clickable = True
        self.timer = 300
        self.ticks = -1
        self.puan = 0
        self.mytime = -1
        self.gameOver = False
        KgameApp.level=1
        self.container.clear_widgets()
        self.fader = Image(source="fader.png", keep_ratio=False, allow_stretch=True, size_hint=(1, 1), opacity=0.95)
        self.add_widget(self.fader)
        anim = Animation(t="out_sine", d=1)
        def fade_gui(ins, val):
            self.generateGUI()
            Clock.schedule_interval(self.countdownTimer, 60 ** -1)
        anim.bind(on_complete=fade_gui)
        anim.start(self.fader)
    def on_enter(self, *args):
        KgameApp.load("sounds/level.ogg")
        self.generateGUI()
        if self.mytime==-1:
            self.timer=300
        else:
            self.timer=self.mytime
        Clock.schedule_interval(self.countdownTimer,60**-1)
    def countdownTimer(self,dt):
        self.timer -=dt
        if self.timer<0.0:
            self.timer = 0
            Clock.unschedule(self.countdownTimer)
            self.gameOver=True
            SoundLoader.load("sounds/end.ogg")
            self.cpanel=EndPanel(auto_dismiss=False)
            self.cpanel.open()
            return
        if KgameApp.level>5:
            self.manager.current="endscreen"
            return
        m,s=divmod(self.timer,60)
        self.countdownL.text="Kalan Süre :%.2i:%.2i"%(m,s)
        self.scoreL.text="Puan : {}".format(self.puan)

    def on_pre_leave(self, *args):
        KgameApp.looper.stop()
        self.mytime=self.timer
        Clock.unschedule(self.countdownTimer)
    def generateGUI(self):
        if self.container.children.__len__()>0:
            return
        level=KgameApp.level
        self.levelL.text="Level :{}".format(level)
        level +=1
        total=2*(level)
        for i in range(total):
            self.imageArray.append(i%level)
        self.myshuffle(self.imageArray)
        self.container.rows=2
        for item in range(total):
            img=ImageButton(num=self.imageArray[item])
            img.bind(on_press=self.clicked)
            self.container.add_widget(img)
            self.objects.append(img)
        if hasattr(self,"fader"):
            self.remove_widget(self.fader)

    def myshuffle(self,aray):
        total=len(aray)
        for x in range(total):
            j=randrange(0,total)
            tmp=self.imageArray[x]
            self.imageArray[x]=self.imageArray[j]
            self.imageArray[j]=tmp

    def clicked(self,instance):
        if not self.clickable:
            return
        self.clickable=False
        self.ticks +=1
        snd=SoundLoader.load("sounds/pop.ogg")
        snd.volume=1
        snd.play()
        myimage=instance
        sizex,sizey=myimage.size
        anim=Animation(t=AnimationTransition.in_sine,d=1,size=(sizex*.8,sizey*0.8))
        def show(instance,val):
            myimage.img.source="images/Jelly{}.png".format(myimage.num)
            myimage.img.keep_ratio=True
            anim=Animation(t=AnimationTransition.out_sine,d=1,size=(sizex,sizey))
            def check_match(instace,val):
                self.flipedImages.append(myimage)
                if self.flipedImages.__len__()<2:
                    self.clickable=True
                if self.flipedImages.__len__()==2:
                    if self.flipedImages[0].num==self.flipedImages[1].num:
                        self.finedImages.extend(self.flipedImages)
                        for froz in self.flipedImages:
                            froz.disabled=True
                        self.puan=self.ticks*10
                        self.clickable=True
                    else:
                        for obj in self.flipedImages:
                            anim=Animation(t=AnimationTransition.in_sine,d=1,size=(sizex*0.8,sizey*0.8))
                            current=obj
                            def load_img(inst,val):
                                val.source="images/f_butn.png"
                                val.keep_ratio = False
                                anim=Animation(t=AnimationTransition.out_sine,size=(sizex,sizey))
                                anim.start(val)
                                self.clickable=True
                            anim.start(current.img)
                            anim.bind(on_complete=load_img)
                        self.puan -=self.ticks*.5
                    self.flipedImages = []
                if self.imageArray.__len__()==self.finedImages.__len__() and len(self.imageArray)>0 and len(self.finedImages)>0:
                    KgameApp.level+=1
                    if KgameApp.level>5:
                        self.manager.current="endscreen"
                        return
                    self.container.clear_widgets()
                    self.fader=Image(source="fader.png",keep_ratio=False,allow_stretch=True,size_hint=(1,1),opacity=0.95)
                    self.add_widget(self.fader)
                    anim = Animation(t="out_sine", d=1)
                    def fade_gui(ins,val):
                        del self.finedImages[:]
                        del self.imageArray[:]
                        self.generateGUI()
                    anim.bind(on_complete=fade_gui)
                    anim.start(self.fader)
            anim.bind(on_complete=check_match)
            anim.start(myimage.img)
        anim.bind(on_complete=show)
        anim.start(myimage.img)

class ScorePanel(ModalView):
    pass
class EndScreen(Screen):
    def postScores(self):
        if hasattr(self,"posts"):
            erp=ErrPanel()
            erp.error.text="Skor Tablosuna daha önce zaten giriş yapıldı!"
            erp.open()
            return
        app=KgameApp.get_running_app()
        game=app.root.get_screen("game")
        nick=self.nick.text
        if len(nick)<3:
            erP=ErrPanel()
            erP.error.text="Nick alanı boş geçilemez\nNick Uzunluğu en az 3 harften oluşmalı!"
            erP.open()
            return
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        data = urlencode({"name": nick, "score": str(game.puan)})
        self.posts=True
        if hasattr(self,"connection"):
            if not self.connection:
                self.nick.text=""
                dbname = "score.db"
                con = sqlite3.connect(dbname)
                sql = "create table if not exists scores(id integer not null primary key autoincrement,ad varchar,puan varchar,tarih datetime)"
                con.execute(sql)
                import time
                now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                sql = "insert into scores(ad,puan,tarih) values('"+str(nick)+"','"+str(game.puan)+"','"+str(now)+"')"
                con.execute(sql)
                con.commit()
                sql="select ad,puan,tarih from scores"
                cursor=con.cursor()
                datas=cursor.execute(sql).fetchall()
                scorePanel = ScorePanel()
                mb = BoxLayout()
                lbl = Label(text="[color=#aef4f3]AD[/color]", markup=True)
                mb.add_widget(lbl)
                lbl = Label(text="[color=#aef4f3]Skor[/color] ", markup=True)
                mb.add_widget(lbl)
                lbl = Label(text="[color=#aef4f3]Tarih[/color] ", markup=True)
                mb.add_widget(lbl)
                scorePanel.container.add_widget(mb)
                for score in datas:
                    bx = BoxLayout()
                    with bx.canvas.before:
                        Color(get_color_from_hex("#abc"))
                    lbl = Label(text=score[0])
                    bx.add_widget(lbl)
                    lbl = Label(text=score[1])
                    bx.add_widget(lbl)
                    tms = time.strptime(score[2], "%Y-%m-%d %H:%M:%S")
                    lbl = Label(text=str(tms.tm_mday) + "." + str(tms.tm_mon) + "." + str(tms.tm_year))
                    bx.add_widget(lbl)
                    scorePanel.container.add_widget(bx)
                scorePanel.container.height = len(datas) * 50
                scorePanel.open()
                return

        UrlRequest(req_headers=headers, req_body=data, url="http://kymath6.coolpage.biz/puzzle.php",
                   on_success=self.posted, on_error=self.error, method="POST")
        try:
            dbname = "score.db"
            con = sqlite3.connect(dbname)
            sql = "select ad,puan from scores"
            cursor = con.cursor()
            all_datas = cursor.execute(sql).fetchall()
            if len(all_datas) > 0:
                for _data in all_datas:
                    data = urlencode({"name": _data[0], "score": str(_data[1])})
                    UrlRequest(req_headers=headers, req_body=data,url="http://kymath6.coolpage.biz/puzzle.php",method="POST")
        except:
            pass
    def error(self,req,data):
        self.connection=False
        erP=ErrPanel()
        erP.error.text="Bağlantı hatası oluştu!\nLocal skor tablosuna kayıt yapılacak!\n"
        erP.open()
    def on_enter(self, *args):
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        UrlRequest(req_headers=headers,method="GET",url="http://www.google.com",on_failure=self.error,on_error=self.error)
    def posted(self,req,data):
        self.nick.text=""
        from time import strptime, strftime, time
        res = json.loads(data.decode()) if not isinstance(data, dict) else data
        scores = res["scores"]
        scorePanel=ScorePanel()
        mb = BoxLayout()
        lbl = Label(text="[color=#aef4f3]AD[/color]", markup=True)
        mb.add_widget(lbl)
        lbl = Label(text="[color=#aef4f3]Skor[/color] ", markup=True)
        mb.add_widget(lbl)
        lbl = Label(text="[color=#aef4f3]Tarih[/color] ", markup=True)
        mb.add_widget(lbl)
        scorePanel.container.add_widget(mb)
        for score in scores:
            bx = BoxLayout()
            with bx.canvas.before:
                Color(get_color_from_hex("#abc"))
            lbl = Label(text=score["ad"])
            bx.add_widget(lbl)
            lbl = Label(text=score["puan"])
            bx.add_widget(lbl)
            tms = strptime(score["zaman"], "%Y-%m-%d %H:%M:%S")
            lbl = Label(text=str(tms.tm_mday) + "." + str(tms.tm_mon) + "." + str(tms.tm_year))
            bx.add_widget(lbl)
            scorePanel.container.add_widget(bx)
        scorePanel.container.height = len(scores) * 50
        scorePanel.open()
        scorePanel.y=-scorePanel.height
        anim=Animation(y=self.height/2-scorePanel.height/2+100,t=AnimationTransition.out_back,d=1)
        def returnBack(anim,val):
            anim=Animation(y=self.height/2-scorePanel.height/2,t=AnimationTransition.in_back,d=1)
            anim.start(scorePanel)
        anim.bind(on_complete=returnBack)
        anim.start(scorePanel)


    def go_back(self):
        app=KgameApp.get_running_app()
        sm=app.root
        sm.current="game"
        game=sm.get_screen("game")
        game.reset()
    def on_pre_leave(self, *args):
        if hasattr(self,"posts"):
            del self.posts

class CikisPanel(ModalView):
    pass
class KgameApp(App):
    volume=0.25
    level=1
    use_kivy_settings = False
    title = "PyPuzzle Oyunu"
    icon = "icon.png"
    def on_pause(self):
        return True
    def on_resume(self):
        return True
    def on_countdown(self,val):
        KgameApp.countdown=val
    def build(self):
        self.root=MScreenManager()
        Window.bind(on_keyboard=self.hook_kb)
        return self.root
    def hook_kb(self, win, key, *largs):
        if key == 27:
            if self.root:
                prev = self.root.previous()
                if prev and str(prev) is not "endscreen":
                    self.root.current = prev
            return True
        return False
    def build_config(self, config):
        config.setdefaults("General",{"sound":"s"})
    def build_settings(self, settings):
        settings.add_json_panel("PyPuzzle Ayar",self.config,data='[{"type":"title","title":"PyPuzzle Ses Ayarı","type":"options","title":"Ses seviyesi","desc":"Oyunun ses ayarlarını 4 seviyeli seçimi yapmaya yarar","section":"General","key":"sound","options":["s","m","l","xl"]}]')

    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "sound":
            vol=0
            if value=="s":
                vol=0.25
            elif value=="m":
                vol=0.5
            elif value=="l":
                vol=0.75
            elif value=="xl":
                vol=1
            self.set_value(val=vol)

    def go(self,txt):
        if txt=="game":
            self.root.current="game"
        elif txt=="ses":
            self.ses()
        elif txt=="hakkimda":
            self.hakkimda()
        elif txt=="exit":
            self.exit()
    def exit(self):
        e=CikisPanel()
        e.open()
        e.x=self.root.width+e.width
        anim=Animation(d=1,t=AnimationTransition.out_sine,center_x=self.root.center_x,center_y=self.root.center_y)
        anim.start(e)

    def hakkimda(self):
        m=AboutPanel()
        m.open()
        m.x=-m.width
        anim=Animation(d=1,t=AnimationTransition.in_sine,center_x=self.root.center_x,center_y=self.root.center_y)
        anim.start(m)
        return
    def ses(self):
        s=SesPanel()
        s.open()
        s.x=-s.width
        anim=Animation(d=1,t=AnimationTransition.in_quart,center_x=self.root.center_x,center_y=self.root.center_y)
        anim.start(s)
        return
    def set_value(self,val):
        KgameApp.volume=val
        KgameApp.looper.volume=val
    @staticmethod
    def load(filename):
        KgameApp.looper=SoundLoader.load(filename)
        KgameApp.looper.volume=KgameApp.volume
        KgameApp.looper.loop=True
        KgameApp.looper.play()



if __name__ == '__main__':
    Builder.load_file("Kgames.kv")
    LabelBase.register(name="ubu",fn_regular="UbuntuMono.ttf")
    KgameApp().run()