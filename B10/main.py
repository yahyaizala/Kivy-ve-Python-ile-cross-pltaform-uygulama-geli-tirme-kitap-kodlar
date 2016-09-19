import RPi.GPIO as gPin
gPin.setmode(gPin.BOARD)
redPin=17
bluePin=27
gPin.setup(redPin,gPin.OUT)
gPin.setup(bluePin,gPin.IN,pull_up_down=gPin.PUD_DOWN)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
class MBoxLayout(BoxLayout):
    pass
class GpioApp(App):
    redTurned=False
    def build(self):
        Clock.schedule_interval(self.checkBlue,1)
        return MBoxLayout()
    def openRed(self):
        self.redTurned=not self.redTurned
        kBtn=self.root.ids.kButton
        if self.redTurned:
            gPin.output(redPin,gPin.HIGH)
            kBtn.text="Kırmızı LED Kapat"
        else:
            gPin.output(redPin,False)#veya gPin.LOW
            kBtn.text="Kırmızı LED Aç"
    def checkBlue(self,nap):
        toggle = self.root.ids["bToggle"]
        if gPin.input(bluePin):
            toggle.state="down"
        elif toggle.state=="down":
            toggle.state="normal"



if __name__ == '__main__':
    GpioApp().run()