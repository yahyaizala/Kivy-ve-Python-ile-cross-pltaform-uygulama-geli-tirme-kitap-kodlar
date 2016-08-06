#!/usr/bin/python
#-*- coding:utf-8 -*-
from xml.dom import minidom
from xml.dom.minidom import parse
DOM = minidom.parse("movie.xml")
collection = DOM.documentElement
print collection
if collection.hasAttribute("etiket"):
   print "Ana element : %s" % collection.getAttribute("etiket")


filmler = collection.getElementsByTagName("film")
for film in filmler:
   print "*****Filmler*****"
   if film.hasAttribute("etiket"):
      print "Etiket: %s" % film.getAttribute("etiket")
   type = film.getElementsByTagName('tip')[0]
   print "Tip: %s" % type.childNodes[0].data
   format = film.getElementsByTagName('format')[0]
   print "Format: %s" % format.childNodes[0].data
   rating = film.getElementsByTagName('rating')[0]
   print "Rating: %s" % rating.childNodes[0].data
   description = film.getElementsByTagName('aciklama')[0]
   print u"Açıklama: %s" % description.childNodes[0].data