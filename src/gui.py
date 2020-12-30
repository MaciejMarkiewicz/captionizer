import PySimpleGUIQt as sg
from viewmodel import ViewModel

WELCOME_TEXT = """Welcome to the Captionizer! 
Press the 'start recording' button to start recording your speaker output
and press stop when you want to stop and begin speech recognition."""
PREFERENCES_MENU = "Preferences"
RECORD_BUTTON = "Record"
STOP_RECORD_BUTTON = "Finish recording"
IN_PROGRESS_BUTTON = "Transcribing..."


class GUI:
    def __init__(self):
        self._view_model = ViewModel()
        self.start_stop_button = sg.Button(button_text=RECORD_BUTTON, size=(50, 8), font='Arial 24', pad=(16, 32))
        self.recognition_result = ""

    def render(self):
        sg.theme('dark')
        menu_def = [['File', [PREFERENCES_MENU]]]
        layout = [[sg.Menu(menu_def, background_color='white')],
                  [sg.Text(WELCOME_TEXT)],
                  [self.start_stop_button]]

        window = sg.Window("Captionizer", layout, element_padding=(16, 16))
        self._event_loop(window)
        window.close()

    def _event_loop(self, window):
        while True:
            event, values = window.read(timeout=1000)

            if event == RECORD_BUTTON:
                self.handle_main_button()
            elif event == sg.WIN_CLOSED:
                break

            if self.recognition_result:
                self._show_result(self.recognition_result)
                self.recognition_result = ""

    def handle_main_button(self):
        if not self._view_model.is_recording:
            self.start_stop_button.update(text=STOP_RECORD_BUTTON)
            self._view_model.on_record_start()
        else:
            self.start_stop_button.update(text=IN_PROGRESS_BUTTON)
            self._view_model.on_record_stop()
            self._view_model.recognize_speech(self._get_recognition_result)

    def _show_result(self, text):
        self.start_stop_button.update(text=RECORD_BUTTON)
        sg.Popup(text, keep_on_top=True)

    def _get_recognition_result(self, result):
        self.recognition_result = result
