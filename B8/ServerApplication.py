from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet.protocol import Protocol,Factory
from twisted.internet import reactor
from kivy.uix.label import Label
from kivy.app import App
host="localhost"
port=8082
class EchoServer(Protocol):
    transports=[]
    def connectionMade(self):
        self.transport.write("\r\nWelcome KServer App\r\n")
        self.transports.append(self.transport)
    def dataReceived(self, data):
        dat=self.factory.app.msg(data)
        for trans in self.transports:
            trans.write(dat)
    def connectionLost(self, reason="connection lost"):
        print "Connection Lost"
class EchoFactory(Factory):
    protocol = EchoServer
    def __init__(self,app):
        self.app=app

class TwistedServer(App):
    def build(self):
        self.lable=Label(text="Server Calisiyor...")
        reactor.listenTCP(port,EchoFactory(self))
        return self.lable
    def msg(self,data):
        self.lable.text +="Veri :%s\r\n"%data
        return data
if __name__ == '__main__':
    TwistedServer().run()