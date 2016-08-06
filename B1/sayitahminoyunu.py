#-*- coding:utf-8 -*-
from random import randrange
tahmin=3
comp_rand=int(randrange(1,10))
print comp_rand
def askQuestion():
    uyari="===Lütfen 1 ile 10 arasında bir sayı giriniz\nsayı===>"
    global sayi
    sayi=input(uyari)
    sayi=int(sayi)
    global tahmin
    tahmin-=1
askQuestion()
bildi=False
while tahmin>=0:
    if sayi == comp_rand:
        print "Doğru bildiniz"
        bildi=True
        break
    else:
        print "Kalan tahmin sayısı :{0}".format(tahmin)
        askQuestion()
if not bildi:
    print "Kaybettiniz!!"



