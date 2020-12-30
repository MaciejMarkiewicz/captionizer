import threading
import os
import json

from multiprocessing.pool import ThreadPool
from recognizer import Recognizer
from recorder import Recorder


class ViewModel:
    def __init__(self):
        self.possible_languages = ["pl-PL", "en-US", "en-GB"]
        self.possible_engines = ["azure", "google"]

        self.is_recording = False
        self._audio_path = os.path.join(os.path.dirname(__file__), 'temp', 'recording.wav')
        self._recording_thread = None
        self._recorder = Recorder(self._audio_path)
        self._recognizer = Recognizer()
        self._settings_path = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir,
                                                            'settings.json'))
        self._settings = self._load_settings()

    def on_record_stop(self):
        self._recorder.stop_recording()
        self.is_recording = False

    def on_record_start(self):
        if not self._recording_thread:
            self.is_recording = True
            self._recording_thread = threading.Thread(
                target=lambda: self._recorder.record(device=self._settings['audio_device']), daemon=True)

            self._recording_thread.start()

    def recognize_speech(self, result_callback):
        self._ensure_recording_finished()
        engine = self._settings['engine']
        ThreadPool(processes=1).apply_async(self._recognizer.speech_to_text,
                                            (self._audio_path, engine, self._settings['engine_settings'][engine]),
                                            callback=result_callback)

    def get_sound_devices(self):
        return self._recorder.get_sound_devices()

    def get_current_engine(self):
        return self._settings['engine']

    def get_current_device(self):
        return self.get_sound_devices()[self._settings['audio_device']]

    def get_language(self, engine=None):
        if engine is None:
            engine = self.get_current_engine()
        return self._settings['engine_settings'][engine]['language']

    def get_region(self, engine=None):
        if engine is None:
            engine = self.get_current_engine()
        return self._settings['engine_settings'][engine].get('region', '')

    def get_key(self, engine=None):
        if engine is None:
            engine = self.get_current_engine()
        return self._settings['engine_settings'][engine].get('key', '')

    def update_settings(self, values):
        print(values)
        engine = values['engine']
        device = self.get_sound_devices().index(values['device'])
        language = values['language']
        region = values['region']
        key = values['key'] if values['key'] is not None else self._settings['engine_settings'][engine]['key']

        self._settings['engine'] = engine
        self._settings['device'] = device
        self._settings['engine_settings'][engine]['language'] = language
        self._settings['engine_settings'][engine]['region'] = region
        self._settings['engine_settings'][engine]['key'] = key

        self._write_settings_to_file(self._settings)

    def _ensure_recording_finished(self):
        self._recording_thread.join()
        self._recording_thread = None

    def _load_settings(self):
        if os.path.exists(self._settings_path):
            with open(self._settings_path) as file:
                return json.load(file)
        else:
            return self._initialize_settings()

    def _initialize_settings(self):
        default_settings = {
            'engine': 'azure',
            'audio_device': 0,
            'engine_settings': {
                'azure': {
                    'language': 'pl-PL',
                    'key': "",
                    'region': 'westus'
                },
                'google': {
                    'key': "",
                    'language': 'pl_PL'
                }
            }
        }

        self._write_settings_to_file(default_settings)
        return default_settings

    def _write_settings_to_file(self, settings):
        with open(self._settings_path, 'w+') as file:
            json.dump(settings, file, indent=2)
