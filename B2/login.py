#-*- coding:utf-8 -*-
from kivy.config import  Config
Config.set("graphics","width","500")
Config.set("graphics","height","800")
Config.set("graphics","resizable","0")
from kivy.app import App
#ana pencere
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty,ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.base import Clock
import urllib
from kivy.clock import mainthread
import re,json
from Users import Loggers
#Builder.load_file("login.kv")
class KullaniciButton(Button):
    to_id=StringProperty()
    imgs=StringProperty()
    user=StringProperty()
class PModalView(ModalView):
    lbl=ObjectProperty()
class KullaniciSayfa(ScrollView):
    pass
class HomePage(AnchorLayout):
    img=StringProperty()
    user=StringProperty()
    to_id=StringProperty()
    msgLabel=ObjectProperty()
    msgInput=ObjectProperty()
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    #url = "http://m.yahyakesenek.com/kycorp/kivy_ky.php"
    url = "http://kymath6.coolpage.biz/kivy.php"
    uniq=None
    def listenMesage(self,dt):
        data=urllib.urlencode({"user_id":Loggers.id,"uniq":self.uniq})
        UrlRequest(url=self.url,method="POST",req_headers=self.headers,req_body=data,on_success=self.msgGeldi,on_error=self.errGeldi)
    def stopListenMsg(self):
        self.uniq=None
        Clock.unschedule(self.listenMesage)
    @mainthread
    def msgGeldi(self,req,data):
        from Utils import timeToStr
        result = json.loads(data.decode("utf-8")) if not isinstance(data, dict) else data
        if result["res"] == "success":
            msgs = result["data"]
            if len(msgs) > 0:
                for msg in msgs:
                    user_id, tm, msg = msg["user_id"], msg["time"], msg["msg"]
                    if user_id == Loggers.id:
                        username = "Ben :"
                        color = "5cacee"
                    else:
                        username = self.user
                        color = "ff7373"
                    _msg = msg + "\n               [size=10][b]" + timeToStr(tm) + "[/b][/size]"
                    self.msgLabel.text += "\n[color=#%s]%s[/color] :\n %s" % (color, username, _msg)
    def startClock(self):
        Clock.schedule_interval(self.checkUniq,1)
    def errGeldi(self,req,data):
        print data
    def getMessages(self):
        data=urllib.urlencode({"user_id":Loggers.id,"to_id":self.to_id})
        UrlRequest(url=self.url,req_headers=self.headers,req_body=data,on_success=self.setFirstLook,on_error=self.errGeldi)
    def checkUniq(self,dt):
        data = urllib.urlencode({"user_id": Loggers.id, "to_id": self.to_id})
        #url="http://m.yahyakesenek.com/kycorp/sendmsg_ky.php"
        url = "http://kymath6.coolpage.biz/sendmsg.php"
        UrlRequest(url=url, req_headers=self.headers,method="POST",req_body=data, on_success=self.getUniq,
                   on_error=self.errGeldi)
    def getUniq(self,req,dt):
        data=json.loads(dt.decode("utf-8")) if not isinstance(dt,dict) else dt
        if data["uniq"]=="not_yet_set":
            return
        if data["uniq"]:
            self.uniq=data["uniq"]
            Clock.unschedule(self.checkUniq)
            Clock.schedule_interval(self.listenMesage, 4)

    def setFirstLook(self,req,data):
        from Utils import timeToStr
        result = json.loads(data) if not isinstance(data, dict) else data
        if result["res"] == "success":
            msgs = result["data"]
            if len(msgs) > 0:
                self.uniq=msgs[0]["uniq"]
                for msg in msgs:
                    user_id, tm, msg = msg["user_id"], msg["time"], msg["msg"]
                    if user_id == Loggers.id:
                        username = "Ben :"
                        color = "5cacee"
                    else:
                        username = self.user
                        color = "ff7373"
                    _msg = msg + "\n               [size=10][b]" + timeToStr(_mytime=tm) + "[/b][/size]"
                    self.msgLabel.text += "\n[color=#%s]%s[/color] :\n %s" % (color, username, _msg)

    def sendMsg(self):
        msg=self.msgInput.text
        msg=msg.strip()
        from Utils import timeString
        if self.uniq:
            data=urllib.urlencode({"msg":msg,"id":Loggers.id,"to_id":self.to_id,"tm":timeString(),"uniq":self.uniq})
        else:
            data=urllib.urlencode({"msg":msg,"id":Loggers.id,"to_id":self.to_id,"tm":timeString()})
        #url="http://m.yahyakesenek.com/kycorp/sendmsg_ky.php"
        url = "http://kymath6.coolpage.biz/sendmsg.php"
        UrlRequest(req_headers=self.headers,url=url,method="POST",req_body=data,on_success=self.localMsg,on_error=self.failed)
    def localMsg(self,req,veri):
        data=json.loads(veri.decode("utf-8")) if not isinstance(veri,dict) else veri
        from Utils import timeString,timeToStr
        tm=timeString()
        if self.uniq:
            scs=data["res"]
            print scs
            if scs=="success":
                msg=self.msgInput.text.strip()
                username="Ben :"
                color="5cacee"
                _msg = msg + "\n               [size=10][b]" + timeToStr(_mytime=tm) + "[/b][/size]"
                self.msgLabel.text += "\n[color=#%s]%s[/color] :\n %s" % (color, username, _msg)
        else:
            if data["res"]=="success":
                if data["uniq"]:
                    self.uniq=data["uniq"]
                    msg = self.msgInput.text.strip()
                    username = "Ben :"
                    color = "5cacee"
                    _msg = msg + "\n               [size=10][b]" + timeToStr(_mytime=tm) + "[/b][/size]"
                    self.msgLabel.text += "\n[color=#%s]%s[/color] :\n %s" % (color, username, _msg)


    def failed(self,req,data):
        print "hata"

class MModalView(ModalView):
    pass
class KModalView(ModalView):
    labeltext=StringProperty()
    def __init__(self,labeltext,**kwargs):
        super(KModalView,self).__init__(**kwargs)
        self.labeltext=labeltext

class LoginApp(App):
    use_kivy_settings = False
    def logIn(self):
        if hasattr(self,"user") and hasattr(self,"psw"):
            if self.user and self.psw:
                self.logUser()
                self.showProgress()

        else:
            self.user=self.root.ids["kullanici"].text
            self.psw=self.root.ids["parola"].text
            if self.validate():
                self.logUser()
                self.showProgress()
            else:
                self.showError()
    def logUser(self):
        login = {"user": self.user, "psw": self.psw}
        import urllib
        login = urllib.urlencode(login)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        #url = "http://m.yahyakesenek.com/kycorp/kivy_ky.php"
        url = "http://kymath6.coolpage.biz/kivy.php"
        UrlRequest(url=url, req_headers=headers, req_body=login, on_success=self.getData, on_error=self.errData)

    def validate(self):
        ptrn = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        match = re.match(ptrn, self.user)
        if match and len(self.psw)>1:
            return True
        else:
            return False
    def showProgress(self,proMes="Yükleniyor..."):
        self.p=PModalView()
        self.p.lbl.text=proMes
        self.p.auto_dismiss=False
        self.p.open()
    def kullaniciListele(self):
        lists = {"list": "getme"}
        import urllib
        lists = urllib.urlencode(lists)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        #url =  "http://m.yahyakesenek.com/kycorp/kivy_ky.php"
        url = "http://kymath6.coolpage.biz/kivy.php"
        UrlRequest(url=url, req_headers=headers, req_body=lists, on_success=self.showUsers, on_error=self.errData)
    def kullaniciSet(self,instance):
        self.root.canvas.clear()
        self.root.clear_widgets()
        self.root.size_hint = (1, 1)
        hp = HomePage()
        hp.to_id, hp.user, hp.img = instance.to_id,instance.user,instance.imgs
        #hp.imgs.source= "http://m.yahyakesenek.com/kycorp/"+str(hp.img)
        hp.imgs.source="http://kymath6.coolpage.biz/images/"+str(hp.img)
        hp.username.text=hp.user
        self.root.add_widget(hp)
        hp.getMessages()
        hp.startClock()

    def showUsers(self,req,data):

        userJ=json.loads(data.decode("utf-8")) if not isinstance(data,dict) else data
        users=userJ["data"]
        self.userSetup=users
        self.root.canvas.clear()
        self.root.clear_widgets()
        self.root.size_hint = (1, 1)
        kullanici = KullaniciSayfa()
        for user in users:
            btn = KullaniciButton()
            btn.user = user["user"]
            btn.to_id = user["id"]
            btn.imgs = user["img"]
            btn.bind(on_release=self.kullaniciSet)
            btn.txt.text = "[font=Roboto][size=15][color=#ffa500]{}[/color][/size][/font]".format(user["user"])
            #btn.img.source =  "http://m.yahyakesenek.com/kycorp/" + str(user["img"])
            btn.img.source = "http://kymath6.coolpage.biz/images/" + str(user["img"])
            kullanici.container.add_widget(btn)
        kullanici.container.height = 100 * len(kullanici.container.children)
        self.root.add_widget(kullanici)
        if self.p:
            self.p.dismiss()
    def userSettedBefore(self,hp):
        if hasattr(self,"userSetup"):
            users=self.userSetup
            self.root.canvas.clear()
            self.root.clear_widgets()
            self.root.size_hint = (1, 1)
            kullanici = KullaniciSayfa()
            for user in users:
                btn = KullaniciButton()
                btn.user = user["user"]
                btn.to_id = user["id"]
                btn.imgs = user["img"]
                btn.bind(on_release=self.kullaniciSet)
                btn.txt.text = "[font=Roboto][size=15][color=#ffa500]{}[/color][/size][/font]".format(user["user"])
                #btn.img.source =  "http://m.yahyakesenek.com/kycorp/"+ str(user["img"])
                btn.img.source = "http://kymath6.coolpage.biz/images/" + str(user["img"])
                kullanici.container.add_widget(btn)
            kullanici.container.height = 100 * len(kullanici.container.children)
            self.root.add_widget(kullanici)
        hp.stopListenMsg()






    def getData(self,req,data):
        print data
        userJ=json.loads(data.decode("utf-8")) if not isinstance(data,dict) else data
        if userJ["res"]=="success" and userJ["data"].__len__()>0:
            id=userJ["data"][0]["id"]
            user=userJ["data"][0]["user"]
            Loggers.id=id
            Loggers.user=user
            self.kullaniciListele()
        else:
            self.showError()
            self.p.dismiss()
    def errData(self,req,data):
        print data,"error"
    def userEnter(self):
        user = self.root.ids["kullanici"].text
        ptrn=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        match = re.match(ptrn, user)
        if match:
            self.user=user
        else:
            self.user=None
            self.showError()

    def passEnter(self):
        psw =str(self.root.ids["parola"].text)
        if len(psw)>0:
            self.psw=psw
        else:
            self.psw=None
            self.showError()
    def showError(self):
        m=MModalView()
        m.open()
        #self.root.ids["kullanici"].focus=True
    def exitOnClick(self,instance=None,val=None):
        uyariModal = KModalView(labeltext="   Uygulamadan çıkmak\nistediğinizden emin misiniz?")
        uyariModal.open()
    def build(self):
        Window.bind(on_keyboard=self.hook_kb)
    def hook_kb(self, win, key, *largs):
        if key == 27:
            self.exitOnClick()
            return True
        elif key in (282, 319):
            print "setting panel goster"
            return True
        return False
    def tester(self):
        print "working"

if __name__ == '__main__':
    Window.clearcolor=(0.3,1,0.3,1)
    LabelBase.register(name="ky",fn_regular="esantial.ttf")
    LoginApp().run()