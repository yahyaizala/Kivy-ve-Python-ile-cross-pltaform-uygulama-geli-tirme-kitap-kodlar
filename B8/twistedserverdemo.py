from twisted.internet.protocol import  DatagramProtocol,Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
class GirisProto(LineReceiver):
    def lineReceived(self, line):
        self.factory.fp.write(line+"\n")
class GirisFactory(Factory):
    protocol = GirisProto
    def __init__(self,dosyaadi):
        self.file=dosyaadi
    def startFactory(self):
        self.fp=open(self.file,"a")
    def stopFactory(self):
        self.fp.close()

class Answer(LineReceiver):
    def lineReceived(self, line):
        self.sendLine("hello")

class Echo(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)
    def connectionMade(self):
        self.transport.write("hello\r\n")
        self.transport.loseConnection()
    def connectionLost(self, reason="connection loast"):
        self.transport.write(reason)
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.internet import reactor
class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo()
endpoint=TCP4ServerEndpoint(reactor,8080)
endpoint.listen(EchoFactory())
reactor.run()