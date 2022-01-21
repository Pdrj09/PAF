import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class myapp(BoxLayout):
    None

class mainApp(App):
    title = 'TARS'

    def build(self):
        return myapp()

mainApp().run()
