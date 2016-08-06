#-*- coding:utf-8 -*-
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivy.core.text import LabelBase
from kivy.uix.label import Label
import json
from kivy.lib import osc
from kivy.clock import Clock
from time import *
from kivy.utils import platform
from kivy.uix.modalview import ModalView
class MPop(ModalView):
    pass
class MWid(Label):
   pass
class MGUI(ScrollView):
    pass
class DovizApp(App):
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    url="http://www.doviz.com/api/v1/currencies/all/latest"
    port=3005
    started=False
    def build(self):
        self.root=MGUI()
        return self.root
    def start_service(self):
        if platform() == 'android':
            from android import AndroidService
            service = AndroidService('DovizApp', 'calisiyor...')
            service.start('service started')
            self.service = service
    def get_currency_from_service(self,currency,*args):
        if str(currency[2])=="update":
            self.request_currency()
        elif str(currency[2]=="error"):
            p=MPop()
            p.lbl.text=currency[2]
            #p.open()
    def load_currency(self,currency):
        self.root.mBox.clear_widgets()
        for x in currency:
            container = MWid()
            ad = x["full_name"]
            alis = str(x["buying"])
            satis = str(x["selling"])
            degisim = "d" if x["change_rate"] > 0 else "u"
            dt = localtime(x["update_date"])
            formated = "%.2d.%.2d.%.4d %.2d:%.2d.%.2d" % (
            dt.tm_mday, dt.tm_mon, dt.tm_year, dt.tm_hour, dt.tm_min, dt.tm_sec)
            tarih = formated
            container.text =u"%s [font=hey]%s[/font] \n Alış : %.5s  Satış : %.5s \n\t\t\t\t\t [i]Tarih :%s [/i]" % (
            ad, degisim, satis, alis, tarih)

            self.root.mBox.add_widget(container)
        self.root.mBox.height = 100 * len(self.root.mBox.children)
    def on_start(self):
        self.request_currency()
    def request_currency(self):
        UrlRequest(self.url, on_success=self.get_curency, req_headers=self.headers, on_error=self.error)
    def get_curency(self,req,data):
        currency=json.loads(data.decode("utf-8")) if  isinstance(data,dict) else data
        self.load_currency(currency)
        if self.started==True:
            return
        self.started=True
        self.service = None
        self.start_service()
        osc.init()
        oscid = osc.listen(port=self.port)#3002
        osc.bind(oscid, self.get_currency_from_service, '/currency')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
    def error(self,req,err):        print err


if __name__ == '__main__':
    LabelBase.register(name="moon",fn_regular="ubuntu.ttf")
    LabelBase.register(name="hey",fn_regular="heydings_icons.ttf")
    DovizApp().run()





'''
[
   {
      "selling":2.9204,
      "update_date":1465854930,
      "currency":1,
      "buying":2.9197,
      "change_rate":0.0181514930459,
      "name":"amerikan-dolari",
      "full_name":"Amerikan Dolar\u0131",
      "code":"USD"
   },
   {
      "selling":3.29754,
      "update_date":1465854914,
      "currency":2,
      "buying":3.29611,
      "change_rate":-0.0154636830855,
      "name":"euro",
      "full_name":"Euro",
      "code":"EUR"
   },
   {
      "selling":4.1537,
      "update_date":1465854918,
      "currency":3,
      "buying":4.1481,
      "change_rate":-0.351458010964,
      "name":"sterlin",
      "full_name":"\u0130ngiliz Sterlini",
      "code":"GBP"
   },
   {
      "selling":2.27675995946,
      "update_date":1465854892,
      "currency":4,
      "buying":2.27585938109,
      "change_rate":-0.0771094096846,
      "name":"kanada-dolari",
      "full_name":"Kanada Dolar\u0131",
      "code":"CAD"
   },
   {
      "selling":0.443393805787,
      "update_date":1465854914,
      "currency":5,
      "buying":0.443189959805,
      "change_rate":0.0542194749672,
      "name":"danimarka-kronu",
      "full_name":"Danimarka Kronu",
      "code":"DKK"
   },
   {
      "selling":0.354387370005,
      "update_date":1465854918,
      "currency":6,
      "buying":0.353937351501,
      "change_rate":0.185087126972,
      "name":"isvec-kronu",
      "full_name":"\u0130sve\u00e7 Kronu",
      "code":"SEK"
   },
   {
      "selling":3.02946058091,
      "update_date":1465854903,
      "currency":7,
      "buying":3.02685050798,
      "change_rate":0.0165899382025,
      "name":"isvicre-frangi",
      "full_name":"\u0130svi\u00e7re Frang\u0131",
      "code":"CHF"
   },
   {
      "selling":0.353537921433,
      "update_date":1465854903,
      "currency":8,
      "buying":0.352620772947,
      "change_rate":0.209132101778,
      "name":"norvec-kronu",
      "full_name":"Norve\u00e7 Kronu",
      "code":"NOK"
   },
   {
      "selling":2.75140849051,
      "update_date":1465854918,
      "currency":9,
      "buying":2.75038622405,
      "change_rate":-0.104453875615,
      "name":"japon-yeni",
      "full_name":"100 Japon Yeni",
      "code":"JPY"
   },
   {
      "selling":0.795403801122,
      "update_date":1465850701,
      "currency":10,
      "buying":0.794723802782,
      "change_rate":0.00680670324135,
      "name":"birlesik-arap-emirlikleri-dirhemi",
      "full_name":"B.A.E. Dirhemi",
      "code":"AED"
   },
   {
      "selling":2.15642336,
      "update_date":1465854907,
      "currency":11,
      "buying":2.15649042,
      "change_rate":0.0135391280801,
      "name":"avustralya-dolari",
      "full_name":"Avustralya Dolar\u0131",
      "code":"AUD"
   },
   {
      "selling":0.0445373025072,
      "update_date":1465854856,
      "currency":12,
      "buying":0.0443956852692,
      "change_rate":0.129262109759,
      "name":"rus-rublesi",
      "full_name":"Rus Rublesi",
      "code":"RUB"
   },
   {
      "selling":9.69266511782,
      "update_date":1465850701,
      "currency":13,
      "buying":9.62644246621,
      "change_rate":0.597014925373,
      "name":"kuveyt-dinari",
      "full_name":"Kuveyt Dinar\u0131",
      "code":"KWD"
   },
   {
      "selling":0.192733872298,
      "update_date":1465854638,
      "currency":14,
      "buying":0.192306932323,
      "change_rate":0.0131747966141,
      "name":"guney-afrika-randi",
      "full_name":"G\u00fcney Afrika Rand\u0131",
      "code":"ZAR"
   },
   {
      "selling":7.75053078556,
      "update_date":1465850701,
      "currency":15,
      "buying":7.74456233422,
      "change_rate":0.0530785562633,
      "name":"bahreyn-dinari",
      "full_name":"Bahreyn Dinar\u0131",
      "code":"BHD"
   },
   {
      "selling":2.14656376332,
      "update_date":1465850702,
      "currency":16,
      "buying":2.13506398537,
      "change_rate":0.219860754855,
      "name":"libya-dinari",
      "full_name":"Libya Dinar\u0131",
      "code":"LYD"
   },
   {
      "selling":0.778773333333,
      "update_date":1465850702,
      "currency":17,
      "buying":0.778482868951,
      "change_rate":0.0413449099081,
      "name":"suudi-arabistan-riyali",
      "full_name":"S. Arabistan Riyali",
      "code":"SAR"
   },
   {
      "selling":0.00250257069409,
      "update_date":1465850702,
      "currency":18,
      "buying":0.00249743370402,
      "change_rate":0.0856164383562,
      "name":"irak-dinari",
      "full_name":"Irak Dinar\u0131",
      "code":"IQD"
   },
   {
      "selling":0.756795978128,
      "update_date":1465854518,
      "currency":20,
      "buying":0.754658946988,
      "change_rate":0.269534793313,
      "name":"israil-sekeli",
      "full_name":"\u0130srail \u015eekeli",
      "code":"ILS"
   },
   {
      "selling":9.69717093904e-5,
      "update_date":1465850702,
      "currency":19,
      "buying":9.67877743155e-5,
      "change_rate":0.079623117245,
      "name":"iran-riyali",
      "full_name":"\u0130ran Riyali",
      "code":"IRR"
   },
   {
      "selling":0.0435335320417,
      "update_date":1465845626,
      "currency":21,
      "buying":0.0434936708861,
      "change_rate":0.561587420442,
      "name":"hindistan-rupisi",
      "full_name":"Hindistan Rupisi",
      "code":"INR"
   },
   {
      "selling":0.155050118926,
      "update_date":1465854915,
      "currency":22,
      "buying":0.154975928491,
      "change_rate":0.0252190741149,
      "name":"meksika-pesosu",
      "full_name":"Meksika Pesosu",
      "code":"MXN"
   },
   {
      "selling":0.0105532468471,
      "update_date":1465854848,
      "currency":23,
      "buying":0.0105187880535,
      "change_rate":0.178651989534,
      "name":"macar-forinti",
      "full_name":"Macar Forinti",
      "code":"HUF"
   },
   {
      "selling":2.060537642,
      "update_date":1465854840,
      "currency":24,
      "buying":2.05859127124,
      "change_rate":0.063496542966,
      "name":"yeni-zelanda-dolari",
      "full_name":"Yeni Zelanda Dolar\u0131",
      "code":"NZD"
   },
   {
      "selling":0.839074845568,
      "update_date":1465854840,
      "currency":25,
      "buying":0.83863277323,
      "change_rate":-0.00287224264705,
      "name":"brezilya-reali",
      "full_name":"Brezilya Reali",
      "code":"BRL"
   },
   {
      "selling":0.000219959328161,
      "update_date":1465854518,
      "currency":26,
      "buying":0.000219741100324,
      "change_rate":-0.285178236398,
      "name":"endonezya-rupiahi",
      "full_name":"Endonezya Rupiahi",
      "code":"IDR"
   },
   {
      "selling":0.12197862325,
      "update_date":1465854918,
      "currency":27,
      "buying":0.121907632954,
      "change_rate":0.0672683212167,
      "name":"cek-korunasi",
      "full_name":"\u00c7ek Korunas\u0131",
      "code":"CSK"
   },
   {
      "selling":0.747517149585,
      "update_date":1465854902,
      "currency":28,
      "buying":0.746382739404,
      "change_rate":0.102359383797,
      "name":"polonya-zlotisi",
      "full_name":"Polonya Zlotisi",
      "code":"PLN"
   },
   {
      "selling":1.5292319619,
      "update_date":1438174813,
      "currency":29,
      "buying":1.52108539945,
      "change_rate":-0.20618556701,
      "name":"bulgar-levasi",
      "full_name":"Bulgar Levas\u0131",
      "code":"BGN"
   },
   {
      "selling":0.73117848827,
      "update_date":1465854818,
      "currency":30,
      "buying":0.729177592967,
      "change_rate":0.140052519695,
      "name":"romen-leyi",
      "full_name":"Romanya Leyi",
      "code":"RON"
   },
   {
      "selling":0.443711828872,
      "update_date":1465850702,
      "currency":31,
      "buying":0.443446955888,
      "change_rate":0.361308026526,
      "name":"cin-yuani",
      "full_name":"\u00c7in Yuan\u0131",
      "code":"CNY"
   },
   {
      "selling":0.21168115942,
      "update_date":1465849236,
      "currency":32,
      "buying":0.211553784861,
      "change_rate":-0.0181061017563,
      "name":"arjantin-pesosu",
      "full_name":"Arjantin Pesosu",
      "code":"ARS"
   },
   {
      "selling":0.0238936605317,
      "update_date":1465846261,
      "currency":33,
      "buying":0.0237754437388,
      "change_rate":0.445716622368,
      "name":"arnavutluk-leki",
      "full_name":"Arnavutluk Leki",
      "code":"ALL"
   },
   {
      "selling":1.9473719184,
      "update_date":1465797614,
      "currency":34,
      "buying":1.94548110764,
      "change_rate":0.433506736028,
      "name":"azerbaycan-manati",
      "full_name":"Azerbaycan Manat\u0131",
      "code":"AZN"
   },
   {
      "selling":1.68313065529,
      "update_date":1465854900,
      "currency":35,
      "buying":1.68030616943,
      "change_rate":0.0892831427666,
      "name":"bosna-hersek-marki",
      "full_name":"Bosna-Hersek Mark\u0131",
      "code":"BAM"
   },
   {
      "selling":0.00014659170766,
      "update_date":1465850702,
      "currency":36,
      "buying":0.000146372888154,
      "change_rate":0.612847090868,
      "name":"belarus-rublesi",
      "full_name":"Belarus Rublesi",
      "code":"BYR"
   },
   {
      "selling":0.00426293481438,
      "update_date":1465831749,
      "currency":37,
      "buying":0.00426070436943,
      "change_rate":0.204274386628,
      "name":"sili-pesosu",
      "full_name":"\u015eili Pesosu",
      "code":"CLP"
   },
   {
      "selling":0.00097574340127,
      "update_date":1465850701,
      "currency":38,
      "buying":0.000974858096828,
      "change_rate":1.93315635423,
      "name":"kolombiya-pesosu",
      "full_name":"Kolombiya Pesosu",
      "code":"COP"
   },
   {
      "selling":0.00544342963653,
      "update_date":1465850702,
      "currency":39,
      "buying":0.00529410698096,
      "change_rate":1.39731568303,
      "name":"kostarika-kolonu",
      "full_name":"Kostarika Kolonu",
      "code":"CRC"
   },
   {
      "selling":0.0265926060827,
      "update_date":1465850702,
      "currency":40,
      "buying":0.0261107136469,
      "change_rate":1.28623188406,
      "name":"cezayir-dinari",
      "full_name":"Cezayir Dinar\u0131",
      "code":"DZD"
   },
   {
      "selling":0.32888128111,
      "update_date":1465850702,
      "currency":41,
      "buying":0.32861741401,
      "change_rate":0.0270197243988,
      "name":"misir-lirasi",
      "full_name":"M\u0131s\u0131r Liras\u0131",
      "code":"EGP"
   },
   {
      "selling":0.376189924128,
      "update_date":1465854898,
      "currency":42,
      "buying":0.376065844045,
      "change_rate":0.00901701639809,
      "name":"hong-kong-dolari",
      "full_name":"Hong Kong Dolar\u0131",
      "code":"HKD"
   },
   {
      "selling":0.440429510768,
      "update_date":1465854896,
      "currency":43,
      "buying":0.435477135101,
      "change_rate":0.578303493073,
      "name":"hirvat-kunasi",
      "full_name":"H\u0131rvat Kunas\u0131",
      "code":"HRK"
   },
   {
      "selling":0.0238123525104,
      "update_date":1465816507,
      "currency":44,
      "buying":0.0236915850004,
      "change_rate":-1.12116601265,
      "name":"izlanda-kronasi",
      "full_name":"\u0130zlanda Kronas\u0131",
      "code":"ISK"
   },
   {
      "selling":4.12078453506,
      "update_date":1465850702,
      "currency":45,
      "buying":4.11109546607,
      "change_rate":0.247018138189,
      "name":"urdun-dinari",
      "full_name":"\u00dcrd\u00fcn Dinar\u0131",
      "code":"JOD"
   },
   {
      "selling":0.00248695874531,
      "update_date":1465817946,
      "currency":46,
      "buying":0.00248443781942,
      "change_rate":0.299017513883,
      "name":"guney-kore-wonu",
      "full_name":"G\u00fcney Kore Wonu",
      "code":"KRW"
   },
   {
      "selling":0.00871690792419,
      "update_date":1465850702,
      "currency":47,
      "buying":0.00871172784244,
      "change_rate":0.00746101619042,
      "name":"kazak-tengesi",
      "full_name":"Kazak Tengesi",
      "code":"KZT"
   },
   {
      "selling":0.00194021522519,
      "update_date":1465850702,
      "currency":48,
      "buying":0.00193083840254,
      "change_rate":0.258534968512,
      "name":"lubnan-lirasi",
      "full_name":"L\u00fcbnan Liras\u0131",
      "code":"LBP"
   },
   {
      "selling":0.0202148828854,
      "update_date":1465817946,
      "currency":49,
      "buying":0.0201731273279,
      "change_rate":-0.0827015851137,
      "name":"sri-lanka-rupisi",
      "full_name":"Sri Lanka Rupisi",
      "code":"LKR"
   },
   {
      "selling":0.976009878285,
      "update_date":1438151715,
      "currency":50,
      "buying":0.974000352299,
      "change_rate":-0.539612460142,
      "name":"litvanya-litasi",
      "full_name":"Litvanya Litas\u0131",
      "code":"LTL"
   },
   {
      "selling":5.43639228043,
      "update_date":1438117198,
      "currency":51,
      "buying":5.40113547377,
      "change_rate":-2.05177372963,
      "name":"letonya-latsi",
      "full_name":"Letonya Lats\u0131",
      "code":"LVL"
   },
   {
      "selling":0.302231237323,
      "update_date":1465854818,
      "currency":52,
      "buying":0.300913138475,
      "change_rate":0.196203969516,
      "name":"fas-dirhemi",
      "full_name":"Fas Dirhemi",
      "code":"MAD"
   },
   {
      "selling":0.14844004065,
      "update_date":1465850702,
      "currency":53,
      "buying":0.147578361982,
      "change_rate":0.559227249619,
      "name":"moldova-leusu",
      "full_name":"Moldovya Leusu",
      "code":"MDL"
   },
   {
      "selling":0.0536418732782,
      "update_date":1465850702,
      "currency":54,
      "buying":0.0534345837145,
      "change_rate":0.718761518614,
      "name":"makedon-dinari",
      "full_name":"Makedon Dinar\u0131",
      "code":"MKD"
   },
   {
      "selling":0.715808823529,
      "update_date":1465850702,
      "currency":55,
      "buying":0.714687882497,
      "change_rate":0.454936677733,
      "name":"malezya-ringgiti",
      "full_name":"Malezya Ringgiti",
      "code":"MYR"
   },
   {
      "selling":7.58649350649,
      "update_date":1465850702,
      "currency":56,
      "buying":7.58099688474,
      "change_rate":0.129971406291,
      "name":"umman-riyali",
      "full_name":"Umman Riyali",
      "code":"OMR"
   },
   {
      "selling":0.878111846061,
      "update_date":1465851300,
      "currency":57,
      "buying":0.875089928058,
      "change_rate":0.633484162896,
      "name":"peru-inti",
      "full_name":"Peru \u0130nti",
      "code":"PEN"
   },
   {
      "selling":0.0632986562635,
      "update_date":1465850702,
      "currency":58,
      "buying":0.0632019917731,
      "change_rate":0.206096105868,
      "name":"filipinler-pesosu",
      "full_name":"Filipinler Pesosu",
      "code":"PHP"
   },
   {
      "selling":0.0279464114833,
      "update_date":1465850702,
      "currency":59,
      "buying":0.0278863419293,
      "change_rate":0.528084493519,
      "name":"pakistan-rupisi",
      "full_name":"Pakistan Rupisi",
      "code":"PKR"
   },
   {
      "selling":0.802257869582,
      "update_date":1465850702,
      "currency":60,
      "buying":0.801762961336,
      "change_rate":0.0384594253063,
      "name":"katar-riyali",
      "full_name":"Katar Riyali",
      "code":"QAR"
   },
   {
      "selling":0.0270259025969,
      "update_date":1465806628,
      "currency":61,
      "buying":0.0268587009564,
      "change_rate":0.159055826938,
      "name":"sirbistan-dinari",
      "full_name":"S\u0131rbistan Dinar\u0131",
      "code":"RSD"
   },
   {
      "selling":2.15448174105,
      "update_date":1465854915,
      "currency":62,
      "buying":2.15348871515,
      "change_rate":0.112236760493,
      "name":"singapur-dolari",
      "full_name":"Singapur Dolar\u0131",
      "code":"SGD"
   },
   {
      "selling":0.0134427059365,
      "update_date":1465849974,
      "currency":63,
      "buying":0.0134204963235,
      "change_rate":0.0459770114943,
      "name":"suriye-lirasi",
      "full_name":"Suriye Liras\u0131",
      "code":"SYP"
   },
   {
      "selling":0.0829894856493,
      "update_date":1465853899,
      "currency":64,
      "buying":0.0828518728717,
      "change_rate":0.184790334044,
      "name":"tayland-bahti",
      "full_name":"Tayland Baht\u0131",
      "code":"THB"
   },
   {
      "selling":0.0901388460352,
      "update_date":1465854300,
      "currency":65,
      "buying":0.0899168207024,
      "change_rate":0.0770772313858,
      "name":"yeni-tayvan-dolari",
      "full_name":"Yeni Tayvan Dolar\u0131",
      "code":"TWD"
   },
   {
      "selling":0.117596618357,
      "update_date":1465849235,
      "currency":66,
      "buying":0.116400956556,
      "change_rate":-0.0597490539733,
      "name":"ukrayna-grivnasi",
      "full_name":"Ukrayna Grivnas\u0131",
      "code":"UAH"
   },
   {
      "selling":0.0947696301103,
      "update_date":1465848067,
      "currency":67,
      "buying":0.0944469598965,
      "change_rate":0.552845528455,
      "name":"uruguay-pesosu",
      "full_name":"Uruguay Pesosu",
      "code":"UYU"
   }
]




'''