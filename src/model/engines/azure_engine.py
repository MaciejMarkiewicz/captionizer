import azure.cognitiveservices.speech as speechsdk
from model.engines.engine import Engine


class AzureEngine(Engine):

    def recognize(self, audio_path, settings, result_callback):
        if not settings['key']:
            result_callback("ERROR: No API key provided")
            result_callback(self.END_VAL)
            return

        speech_config = speechsdk.SpeechConfig(subscription=settings['key'], region=settings['region'])
        audio_input = speechsdk.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input,
                                                       language=settings['language'])

        def end_callback(evt):
            nonlocal audio_input
            nonlocal speech_recognizer

            speech_recognizer.stop_continuous_recognition()
            result_callback(self.END_VAL)

            # fix thread not releasing audio file
            speech_recognizer = None
            audio_input = None

        speech_recognizer.recognized.connect(lambda evt: result_callback(evt.result.text))
        speech_recognizer.session_stopped.connect(end_callback)

        speech_recognizer.start_continuous_recognition()
