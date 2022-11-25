import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations


class BrainflowData:
    def __init__(self, sf=16):
        BoardShim.enable_dev_board_logger()
        # using synthetic board 
        self.params = BrainFlowInputParams()
        self.board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, self.params)

        self.board_id = BoardIds.SYNTHETIC_BOARD.value
        self.sf = sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        
        self.eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
        self.eeg_names = BoardShim.get_eeg_names(BoardIds.SYNTHETIC_BOARD.value)
        self.x_data = []
        self.stop_flow = False

    def start(self):
        self.board.prepare_session()
        self.board.start_stream()
        print('started streaming!! ')
        # time.sleep(2)
        
    def data_gen(self):
        data = self.board.get_board_data(16) 
        print(self.eeg_names)

    def stop(self):
        self.stop_flow = True
        self.x_data = []
        self.board.stop_stream()
        self.board.release_session()
        print('streaming stopped!! ')

class MyDisplayData(BoxLayout, BrainflowData):
    display_text = StringProperty('Start Connection')
    connect_stream = BooleanProperty(True)
    data_stream = BooleanProperty(False)
    b_flow = BrainflowData()
    
    def on_btn_start(self):
        if self.connect_stream:
            self.b_flow.start()
            self.display_text = 'Connected... Stream to display data'
            self.connect_stream = False
            self.data_stream = True
    
    def on_btn_data_stream(self):
        if self.data_stream:
            self.b_flow.data_gen()
            self.data_stream = False
            self.display_text = str(self.b_flow.eeg_names)

    def on_btn_stop(self):
        self.b_flow.stop()
        self.display_text = 'Start Connection'
        self.connect_stream = True
        self.data_stream = False
        
class MainApp(App):
    def build(self):
        return MyDisplayData()
      
if __name__ == "__main__":
    MainApp().run()
