from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet.protocol import Protocol,ClientFactory
from twisted.internet import reactor
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
host="localhost"
port=8082
class EchoProtocol(Protocol):
    def dataReceived(self, data):
        self.factory.app.msg_recieved(data)
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
    def connectionLost(self, reason="failed"):
        print "connection lost"
class EchoFactory(ClientFactory):
    protocol = EchoProtocol
    def __init__(self,app):
        self.app=app
    def clientConnectionLost(self, connector, reason):
        print "connection lost",reason
    def clientConnectionFailed(self, connector, reason):
        print "connection failed",reason

class GuiApp(App):
    connection=None
    nick=""
    def build(self):
        self.gui()
        Clock.schedule_once(self.show_modal,1)
    def show_modal(self,dt):
        modal=ModalView(size_hint=(0.5,.3),auto_dismiss=False)
        modalBox=BoxLayout(orientation="vertical",spacing=5,padding=10)
        txt=TextInput(hint_text="Takma ad giriniz...",size_hint=(1,None),height=50)
        modalBox.add_widget(txt)
        modalBtn=Button(text="Tamam",size_hint=(1,None),height=50)
        def setNick(instance):
            self.setted=True
            self.nick=txt.text
            modal.dismiss()
            self.root.opacity=1
            self.connect_to_server()
        modalBtn.bind(on_release=setNick)
        modalBox.add_widget(modalBtn)
        modal.add_widget(modalBox)
        modal.open()

    def gui(self):
        self.root=BoxLayout(orientation="vertical",padding=2,spacing=3)
        scrol=ScrollView(size_hint=(1,0.8))
        self.lbl=None
        self.lbl=Label(text="Mesaj Yok!",halign="left",valign="top",markup=True)
        scrol.add_widget(self.lbl)
        self.inpt=TextInput(size_hint=(6,1))
        btn=Button(size_hint=(1,1),text="Gonder",on_press=self.send_msg)
        self.root.add_widget(scrol)
        mbox=BoxLayout(size_hint=(1,.1))
        mbox.add_widget(self.inpt)
        mbox.add_widget(btn)
        self.root.add_widget(mbox)
        self.root.opacity=0
        return self.root
    def connect_to_server(self):
        reactor.connectTCP(host,port,EchoFactory(self))
    def send_msg(self,instance):
        msg=self.nick+":"+str(self.inpt.text)
        if msg and self.connection:
            self.connection.write(str(msg))
        self.inpt.text=""
    def on_connection(self,connection):
        self.connection=connection
    def msg_recieved(self,msg):
        self.lbl.text +=msg+"\r\n"
if __name__ == '__main__':
    GuiApp().run()