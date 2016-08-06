class Personel(object):
    @classmethod
    def odemeYap(cls,personel,maas):
        # This method can be used as an instance or static method.
        print "{0} personelinin hesabina {1} yatirildi.".format(personel,maas)
    def islemBasirili(self):
        print "islem bitti"


Personel.odemeYap("yahya",7600.0)
p=Personel()
p.odemeYap("muhittin",6000.0)