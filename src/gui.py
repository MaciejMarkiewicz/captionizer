import PySimpleGUIQt as sg
from viewmodel import ViewModel

WELCOME_TEXT = """Welcome to the Captionizer! 
Press the "Record" button to start recording your speaker output
and press stop when you want to stop and begin speech recognition."""
PREFERENCES_MENU = "Preferences"
RECORD_BUTTON = "Record"
STOP_RECORD_BUTTON = "Finish recording"
IN_PROGRESS_BUTTON = "Transcribing..."
EMPTY_RESULT_TEXT = "Error: the speech recognition engine could not recognize anything"
APPLY_BUTTON = "Apply"
ENGINE_DROP = 'engine'
DEVICE_DROP = 'device'
KEY_INPUT = 'key'
LANGUAGE_DROP = 'language'
REGION_INPUT = 'region'
DEFAULT_KEY_TEXT = 'Key is not shown to keep it secure'


class GUI:
    def __init__(self):
        self._view_model = ViewModel()
        self.start_stop_button = sg.Button(button_text=RECORD_BUTTON, size=(50, 8), font='Arial 24', pad=(16, 32))
        self.recognition_result = None

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
            elif event == PREFERENCES_MENU:
                self.show_preferences()
            elif event == sg.WIN_CLOSED:
                break

            if self.recognition_result is not None:
                self._show_result(self.recognition_result)
                self.recognition_result = None

    def handle_main_button(self):
        if not self._view_model.is_recording:
            self.start_stop_button.update(text=STOP_RECORD_BUTTON)
            self._view_model.on_record_start()
        else:
            self.start_stop_button.update(text=IN_PROGRESS_BUTTON, disabled=True)
            self._view_model.on_record_stop()
            self._view_model.recognize_speech(self._get_recognition_result)

    def _show_result(self, text):
        self.start_stop_button.update(text=RECORD_BUTTON, disabled=False)
        sg.Popup(text or EMPTY_RESULT_TEXT, keep_on_top=True)

    def _get_recognition_result(self, result):
        self.recognition_result = result

    def show_preferences(self):
        layout = [[sg.Text("Settings:")],
                  [sg.Text("Speech recognition engine:"), sg.Drop(self._view_model.possible_engines, readonly=True,
                                                                  default_value=self._view_model.get_current_engine(),
                                                                  key=ENGINE_DROP, enable_events=True)],
                  [sg.Text("Sound device:"), sg.Drop(self._view_model.get_sound_devices(), readonly=True,
                                                     default_value=self._view_model.get_current_device(),
                                                     key=DEVICE_DROP)],
                  [sg.Text("Engine specific settings:")],
                  [sg.Text("API key:"), sg.In(key=KEY_INPUT, default_text=DEFAULT_KEY_TEXT)],
                  [sg.Text("Language:"), sg.Drop(self._view_model.possible_languages, key=LANGUAGE_DROP,
                                                 default_value=self._view_model.get_language())],
                  [sg.Text("Region (optional):"), sg.In(key=REGION_INPUT, default_text=self._view_model.get_region())],
                  [sg.Button(APPLY_BUTTON)]]

        window = sg.Window("Preferences", layout)

        while True:
            event, values = window.read()

            if event == ENGINE_DROP:
                window.find_element(LANGUAGE_DROP).update(self._view_model.get_language(values[ENGINE_DROP]))
                window.find_element(REGION_INPUT).update(self._view_model.get_region(values[ENGINE_DROP]))
            elif event == APPLY_BUTTON:
                if values[KEY_INPUT].strip() == DEFAULT_KEY_TEXT:
                    values[KEY_INPUT] = None

                self._view_model.update_settings(values)
                break
            elif event == sg.WIN_CLOSED:
                break

        window.close()
