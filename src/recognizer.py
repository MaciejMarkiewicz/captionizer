import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk


class Recognizer:
    def speech_to_text(self, audio_path, engine, settings):
        engines = {
            'google': self._recognize_google,
            'azure': self._recognize_azure
        }

        return engines[engine](audio_path, settings)

    @staticmethod
    def _recognize_google(audio_path, settings):
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            return recognizer.recognize_google(audio, key=settings['key'] or None, language=settings['language'])
        except sr.UnknownValueError:
            return "ERROR: An error occurred during processing"

    @staticmethod
    def _recognize_azure(audio_path, settings):
        speech_config = speechsdk.SpeechConfig(subscription=settings['key'], region=settings['region'])
        audio_input = speechsdk.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input,
                                                       language=settings['language'])

        result = speech_recognizer.recognize_once()
        return result.text

