#-*- coding:utf-8 -*-
a=(1,2,3,4,5)
print a
#(1, 2, 3, 4, 5)
b=("x","y",3)
c=a+b
print c.count(3)
#2 adet 3 içeriyor.
print a[2]
#3
f_item,s_item=a[0],a[1]
print "birinci değişken :%i ikinci değişken %i "%(f_item,s_item)
#birinci değişken :1 ikinci değişken 2
print "A tuple max değeri :%s"%max(a)
#birinci değişken :1 ikinci değişken 2
print "A tuple min değeri :%s"%min(a)
#birinci değişken :1 ikinci değişken 2
print "B tuple eleman sayısı :%s"%len(b)
#B tuple eleman sayısı :3
print "B tuple en büyük  elemanı :%s"%max(b)
#B tuple en büyük  elemanı :y
print "A ile B tuple aynı mı :%d"%cmp(a,b)
#A ile B tuple aynı mı :-1(False)
a[0]=2
'''Traceback (most recent call last):

  File "C:/Users/FREE/Desktop/pthn/Book/B0/ltuple.py", line 24, in <module>

    a[0]=2
'''
