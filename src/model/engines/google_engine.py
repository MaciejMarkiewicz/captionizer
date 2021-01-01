from model.engines.engine import Engine
import speech_recognition as sr


class GoogleEngine(Engine):

    def recognize(self, audio_path, settings, result_callback):
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
