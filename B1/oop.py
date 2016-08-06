class Dikdortgen(object):
    def __init__(self,kisaKenar,uzunKenar):
        self.uzun_kenar = uzunKenar
        self.kisa_kenar = kisaKenar
        return self.kisa_kenar,self.uzun_kenar
    def alan(self):
        return self.uzun_kenar*self.kisa_kenar
    def cevre(self):
        return 2*(self.kisa_kenar+self.uzun_kenar)
class Kare(Dikdortgen):
    def __init__(self,**kwargs):
        super(Kare,self).__init__(**kwargs)
        self.uzun_kenar=self.kisa_kenar
#k=Kare(kisaKenar=3,uzunKenar=5)
#print k.alan()

class Arabac(object):
    static_degisken=0
    def __init__(self,**kwargs):
        self.model=kwargs.get("model")
        self.yil=kwargs.get("yil")
        self.marka=kwargs.get("marka")
    def printer(self):
        print self.model,self.marka,self.yil
    @staticmethod
    def calis(cls,msg="Working"):
        cls.calis(msg=msg)
    @classmethod
    def calisC(cls,msg):
        cls.calis(msg=msg)
class Kamyon(object):
    def calis(self,msg):
        print msg

class Otomobil(Arabac):
    def __init__(self,motor,**kwargs):
        super(Otomobil,self).__init__(**kwargs)
        self.motor=motor
k=Otomobil(motor="123",model="civic",yil=1982,marka="Honda")
k.printer()
print k.static_degisken
k.static_degisken=12
Arabac.static_degisken=35
print k.static_degisken
print Arabac.static_degisken
print Arabac.static_degisken
print k.static_degisken
kamyon=Kamyon()
Arabac.calis(kamyon,msg="kamyon calisti")

