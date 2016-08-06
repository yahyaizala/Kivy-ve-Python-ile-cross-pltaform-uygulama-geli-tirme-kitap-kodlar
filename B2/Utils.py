#-*- coding:utf-8 -*-
import time

def timeToStr(_mytime="06-03-2015 15:52:00"):
    mytime=_mytime
    mytime=time.strptime(mytime,"%Y-%m-%d %H:%M:%S")
    now=time.localtime(time.time())
    if now.tm_year-mytime.tm_year>0:
        return u"{} yil önce gönderildi.".format(now.tm_year-mytime.tm_year)
    elif now.tm_mon-mytime.tm_mon>0:
        return u"{} ay önce gönderildi.".format(now.tm_mon-mytime.tm_mon)
    elif now.tm_mday-mytime.tm_mday>0:
        return u"{} gün önce gönderilidi.".format(now.tm_mday-mytime.tm_mday)
    elif now.tm_hour-mytime.tm_hour>0:
        minute=(now.tm_hour-mytime.tm_hour+60) if now.tm_hour-mytime.tm_hour<0 else now.tm_hour-mytime.tm_hour
        return u"{} saat {} dakika önce gönderildi.".format(now.tm_hour-mytime.tm_hour,minute)
    elif now.tm_min-mytime.tm_min>0:
        second = (now.tm_sec - mytime.tm_sec + 60) if now.tm_sec - mytime.tm_sec < 0 else now.tm_sec - mytime.tm_sec
        return u"{} dakika {} saniye önce gönderildi.".format(now.tm_min-mytime.tm_min,second)
    elif now.tm_sec-mytime.tm_sec>0:
        return u"{} saniye önce gönderildi.".format(now.tm_sec-mytime.tm_sec)
    else:
        return u"0 saniye önce gönderildi."
def timeString():
    lcl=time.localtime(time.time())
    return time.strftime("%Y-%m-%d %H:%M:%S",lcl)




'''
print timeToStr()
print timeToStr(_mytime="05-03-2016 15:52:19")
print timeToStr(_mytime="06-02-2016 15:52:19")
print timeToStr(_mytime="06-03-2016 16:12:59")
print timeToStr(_mytime="06-03-2016 16:24:55")
'''
