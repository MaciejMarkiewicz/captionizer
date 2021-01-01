from model.engines.google_engine import GoogleEngine
from model.engines.azure_engine import AzureEngine


class Recognizer:

    def speech_to_text(self, audio_path, engine, settings, result_callback):
        engines = {
            'google': GoogleEngine,
            'azure': AzureEngine
        }

        return engines[engine]().recognize(audio_path, settings, result_callback)
