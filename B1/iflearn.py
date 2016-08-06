#-*- coding:utf-8 -*-
from random import randrange
tahmin=3
comp_rand=randrange(1,10)
uyari="===Lütfen 1 ile 10 arasında bir sayı giriniz\nsayı===>"
sayi=input(uyari)
sayi=int(sayi)
if sayi==comp_rand:
    print "Doğru bildiniz"
else:
    tahmin -=1
    print "Kalan tahmin sayısı :{0}".format(tahmin)
    sayi=int(input(uyari))
    if sayi==comp_rand:
        print "Doğru bildiniz"
    else:
        tahmin -= 1
        print "Kalan tahmin sayısı :{0}".format(tahmin)
        sayi = int(input(uyari))
        if sayi==comp_rand:
            print "Doğru bildiniz"
        else:
            print "Kaybettiniz!!"

