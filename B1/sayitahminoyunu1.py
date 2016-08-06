#-*- coding:utf-8 -*-
from random import randrange
tahmin=2
comp_rand=int(randrange(1,10))
uyari="===Lütfen 1 ile 10 arasında bir sayı giriniz\nsayı===>"
sayi=input(uyari)
sayi=int(sayi)
while tahmin>0:
	if sayi == comp_rand:
		print "Doğru bildiniz"
		break
	else:
		print "Kalan tahmin sayısı :{0}".format(tahmin)
		tahmin -= 1
		sayi = int(input(uyari))
		if tahmin<1:
			print "Kaybettiniz!!"
