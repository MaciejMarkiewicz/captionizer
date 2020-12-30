import threading
import os
import json

from multiprocessing.pool import ThreadPool
from recognizer import Recognizer
from recorder import Recorder


class ViewModel:
    def __init__(self):
        self.is_recording = False
        self._audio_path = os.path.join(os.path.dirname(__file__), 'temp', 'recording.wav')
        self._recorder = Recorder(self._audio_path)
        self._recognizer = Recognizer()
        self._settings = self._load_settings()
        self._recording_thread = threading.Thread(target=self._recorder.record, daemon=True)

    def on_record_stop(self):
        self._recorder.stop_recording()
        self.is_recording = False

    def on_record_start(self):
        if not self._recording_thread.is_alive():
            self.is_recording = True
            self._recording_thread.start()

    def recognize_speech(self, result_callback):
        self._recording_thread.join()
        engine = self._settings['engine']
        ThreadPool(processes=1).apply_async(self._recognizer.speech_to_text,
                                            (self._audio_path,
                                             engine,
                                             self._settings['engine_settings'][engine]),
                                            callback=result_callback)

    def _load_settings(self):
        settings_path = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, 'settings.json'))

        if os.path.exists(settings_path):
            with open(settings_path) as file:
                return json.load(file)
        else:
            return self._initialize_settings(settings_path)

    def _initialize_settings(self, settings_path):
        settings = {
            'engine': 'azure',
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

        with open(settings_path, 'w+') as file:
            json.dump(settings, file, indent=2)

        return settings

