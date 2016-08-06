#-*- coding:utf-8 -*-
from requests import request
from kivy.network.urlrequest import UrlRequest
import json,time

apiID="1ed2941a8009a0a2254067fbcc9f34fb"
url="http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=%s"%apiID
def onComplete(req,data):
    print data
UrlRequest(url=url,on_success=onComplete)


req=request("GET",url)
if req.status_code==200:
    weather=json.loads(req.text)
    city=weather["city"]["name"]
    lat=weather["city"]["coord"]["lat"]
    lon=weather["city"]["coord"]["lon"]
    main=weather["list"][0]["weather"][0]["main"]
    tm=weather["list"][0]["dt"]
    tm=time.localtime(tm)
    description=weather["list"][0]["weather"][0]["description"]
    print "*"*10+"{0} Hava Durum Raporu ".format(city)+"*"*10
    print "===Koordinatlar : ({},{} ) ".format(lat,lon)
    print "==={} satindeki Hava Durumu :{}".format(tm.tm_hour,main)
    print "===Açıklama : {} ".format(description)
    print "===Saniyeden Çevrilen Tam Tarih Değeri :{}".format(time.strftime("%d/%m/%Y %H:%S"),tm)
'''
**********Moscow Hava Durum Raporu **********
===Koordinatlar : (55.75222,37.615555 )
===0 satindeki Hava Durumu :Clear
===Açıklama : clear sky
===Saniyeden Çevrilen Tam Tarih Değeri :31/05/2016 23:37

'''




