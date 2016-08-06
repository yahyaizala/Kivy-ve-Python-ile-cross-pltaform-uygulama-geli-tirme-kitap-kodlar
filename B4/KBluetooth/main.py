from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from jnius import autoclass
import sys
from android.runnable import run_on_ui_thread
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')
class MModal(ModalView):
    pass
class MPop(ModalView):
    err_str=StringProperty()

class GUI(GridLayout):
    def send(self, txt):
        self.send_stream.write('{}\n'.format(txt))
        self.send_stream.flush()
        self.openErr(txt="Gonderildi"+str(txt))
    def openconnection(self):
        m = MModal()
        m.open()
    def openErr(self,txt):
        p = MPop()
        p.err_str = txt
        p.open()
    @run_on_ui_thread
    def connect(self,cihaz_adi):
        cihaz=cihaz_adi
        try:
            self.recv,self.snd=self.get_socket(cihaz)
        except AttributeError as e:
            self.openErr(e.message)
        except jnius.JavaException as e:
            self.openErr(e.message)
        except:
            self.openErr(sys.exc_info()[0])
            return False
    @run_on_ui_thread
    def get_socket(self, cihaz):
        tum_chihazlar = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        socket = None
        for device in tum_chihazlar:
            if device.getName() == cihaz:
                socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                recv = socket.getInputStream()
                snd = socket.getOutputStream()
                break
        socket.connect()
        return recv, snd


class KBluetoothApp(App):
    def build(self):
        self.root=GUI()
        return self.root
    def on_start(self):
        self.root.openconnection()
    def connect(self,inst,device):
        inst.dismiss()
        self.root.connect(device)

if __name__ == '__main__':
    KBluetoothApp().run()