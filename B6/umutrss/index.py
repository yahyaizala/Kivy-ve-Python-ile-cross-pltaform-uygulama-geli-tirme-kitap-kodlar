#-*- coding:utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
Builder.load_file("index.kv")
class MButton(Button):
    urls=None
class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        js=JsonStore(filename="UmutRss.json")
        js.put("current_rss",title=u"Haber Türk",url={"gundem": "http://www.haberturk.com/rss/manset.xml",
                                                "siyaset": "http://www.haberturk.com/rss/siyaset.xml",
                                                "dunya": "http://www.haberturk.com/rss/dunya.xml",
                                                "yasam": "http://www.haberturk.com/rss/yasam.xml",
                                                "sanat": "http://www.haberturk.com/rss/kultur-sanat.xml",
                                                "ekonomi": "http://www.haberturk.com/rss/ekonomi.xml",
                                                "spor": "http://www.haberturk.com/rss/spor.xml"})
        js.put("Sabah",title="Sabah",url={"gundem": "http://www.sabah.com.tr/rss/gundem.xml",
                     "saglik": "http://www.sabah.com.tr/rss/saglik.xml",
                     "dunya": "http://www.sabah.com.tr/rss/dunya.xml",
                     "sanat": "http://www.sabah.com.tr/rss/kultur_sanat.xml",
                     "ekonomi": "http://www.sabah.com.tr/rss/ekonomi.xml",
                     "spor": "http://www.sabah.com.tr/rss/spor.xml",
                     "yasam": "http://www.sabah.com.tr/rss/yasam.xml",
                     "oyun": "http://www.sabah.com.tr/rss/oyun.xml",
                     "sondakika": "http://www.sabah.com.tr/rss/sondakika.xml",
                     "teknoloji": "http://www.sabah.com.tr/rss/teknoloji.xml"})
        js.put("BBC",title="BBC",url={"gundem": "http://feeds.bbci.co.uk/turkce/rss.xml"
                                      })
        js.put("Cmh",title="Cumhuriyet",url={"egitim":"http://www.cumhuriyet.com.tr/rss/18.xml",
                                             "yasam":"http://www.cumhuriyet.com.tr/rss/10.xml",
                                             "sanat":"http://www.cumhuriyet.com.tr/rss/7.xml",
                                             "dunya":"http://www.cumhuriyet.com.tr/rss/5.xml",
                                             "sondakika":"http://www.cumhuriyet.com.tr/rss/son_dakika.xml",
                                             "gundem":"http://www.cumhuriyet.com.tr/rss/1.xml"

        })
        js.put("AHaber",title="A Haber",url={"gundem": "http://www.ahaber.com.tr/rss/gundem.xml",
                                      "ekonomi": "http://www.ahaber.com.tr/rss/ekonomi.xml",
                                      "spor": "http://www.ahaber.com.tr/rss/spor.xml",
                                       "saglik": "http://www.ahaber.com.tr/rss/saglik.xml",
                                        "dunya": "http://www.ahaber.com.tr/rss/dunya.xml",
                                        "manset": "http://www.ahaber.com.tr/rss/haberler.xml",
                                        "yasam": "http://www.ahaber.com.tr/rss/yasam.xml",
                                        "anasayfa": "http://www.ahaber.com.tr/rss/anasayfa.xml",
                                        "ozelhaber": "http://www.ahaber.com.tr/rss/ozel-haberler.xml",
                                        "teknoloji": "http://www.ahaber.com.tr/rss/teknoloji.xml"
                                           })

        titles=JsonStore(filename="titles.json")
        titles.put("titles",all={"gundem":u"Gündem","egitim":u"Eğitim","dunya":u"Dünya","sanat":u"Sanat",
                                 "ekonomi":u"Ekonomi","spor":u"Spor","saglik":u"Sağlık","yasam":u"Yaşam",
                                 "oyun":u"Oyun","sondakika":u"Son Dakika","teknoloji":u"Teknoloji",
                                 "basinozeti":u"Basın Özeti","ozelhaber":u"Özel Haber","anasayfa":"Anasayfa",
                                 "turkiye":u"Türkiye","siyaset":"Siyaset","manset":u"Manşet"})




    def on_enter(self, *args):
        feeds=JsonStore("UmutRss.json")
        if len(self.grid.children)>0:
            self.grid.clear_widgets()
        self.grid.bind(minimum_height=self.grid.setter("height"))
        for feed in feeds.keys():
            title=feeds.get(feed)["title"]
            url=feeds.get(feed)["url"]
            btn=MButton(text=title,height=65)
            btn.urls=url
            btn.bind(on_press=self.next_screen)
            self.grid.add_widget(btn)
    def next_screen(self,inst):
        from home import HomeScreen
        HomeScreen.urls=inst.urls
        HomeScreen.title=inst.text
        self.manager.current="homescreen"












