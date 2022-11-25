import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder

class MyDisplayData(BoxLayout):
    display_text = StringProperty('Start display')
    connect_stream = BooleanProperty(True)
    data_stream = BooleanProperty(False)
    
    def on_btn_start(self):
        if self.connect_stream:
            self.display_text = 'Displaying data start'
            self.connect_stream = False
            self.data_stream = True
    
    def on_btn_data_stream(self):
        if self.data_stream:
            self.data_stream = False
            i = 0
            x = []
            while True:
                if i == 10:
                    break
                time.sleep(0.1)
                x.append(i)
                i += 1
            self.display_text = str(x)

    def on_btn_stop(self):
        self.display_text = 'Displaying data stopped!'
        self.connect_stream = True
        self.data_stream = False
        
class MainApp(App):
    def build(self):
        return MyDisplayData()
      
if __name__ == "__main__":
    MainApp().run()