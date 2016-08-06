from kivy.lib import osc
from time import sleep
from requests import request
import json
def currency():
    url = "http://www.doviz.com/api/v1/currencies/all/latest"
    req = request(url=url, method="GET")
    update="noupdate"
    if req.status_code == 200:
        js = json.loads(req.text)
        for x in js:
            if abs(x["change_rate"])>0.02 and (x["name"]=="amerikan-dolari" or x["name"]=="euro" or x["name"]=="sterlin") :
                update="update"
                try:
                    from utils2 import AndroidNotification
                    title = "Doviz App"
                    message = "{} {} yukseldi".format(x["name"], x["change_rate"])
                    notify=AndroidNotification()
                    notify._notify(title=title,message=message,ticker="Doviz App Yeni")
                except:
                    update="error"
                break
    port = 3005
    js=[str(update),]
    osc.sendMsg('/currency',js,port=port)

if __name__ == '__main__':
    osc.init()
    port = 3004
    oscid = osc.listen(ipAddr='0.0.0.0', port=port)
    while True:
        osc.readQueue(oscid)
        currency()
        sleep(1)