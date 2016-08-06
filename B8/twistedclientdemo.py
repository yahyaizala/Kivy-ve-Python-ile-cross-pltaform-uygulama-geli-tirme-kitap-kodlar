from twisted.internet.protocol import Protocol,ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
host="localhost"
port=8081
class MProto(Protocol):
    def dataReceived(self, data):
        self.transport.write("Merhaba sunucu\r\n")
        self.transport.loseConnection()
class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print "baglaniyor...."
    def buildProtocol(self, addr):
        return MProto()
    def clientConnectionLost(self, connector, reason):
        print "connection failes :",reason
    def clientConnectionFailed(self, connector, reason):
        print "connection failed",reason
reactor.connectTCP(host,port,EchoClientFactory())
reactor.run()