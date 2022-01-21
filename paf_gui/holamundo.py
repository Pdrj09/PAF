import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.button import Button
from functools import partial

class myButton(App):
    
    def disable(self, instance, *args):
        instance.disabled = True


    def update(self, instance, *args):
        instance.text = 'Off'

    def build(self):
        mybtn = Button(text='On')

        mybtn.bind(on_press=partial(self.disable, mybtn))
        mybtn.bind(on_press=partial(self.update, mybtn))

        return mybtn

myButton().run()
