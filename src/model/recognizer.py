import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk


class Recognizer:
    END_VAL = "<END>"

    def speech_to_text(self, audio_path, engine, settings, result_callback):
        engines = {
            'google': self._recognize_google,
            'azure': self._recognize_azure
        }

        return engines[engine](audio_path, settings, result_callback)

    def _recognize_google(self, audio_path, settings, result_callback):
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            result = recognizer.recognize_google(audio, key=settings['key'] or None, language=settings['language'])
            result_callback(result)
        except sr.UnknownValueError:
            result_callback("ERROR: The engine could not recognize anything")
        except sr.RequestError as e:
            result_callback(f"ERROR: An error occurred during processing. Details: {e}")
        finally:
            result_callback(self.END_VAL)

    def _recognize_azure(self, audio_path, settings, result_callback):
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
