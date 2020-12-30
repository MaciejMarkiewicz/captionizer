import os
import queue

import sounddevice as sd
import soundfile as sf
import numpy  # import needed


class Recorder:

    def __init__(self, audio_path):
        self.recording = False
        self.audio_path = audio_path

    def record(self, device, samplerate=16000):
        def _callback(indata, frames, time, status):
            q.put(indata.copy())

        self.recording = True

        q = queue.Queue()

        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)

        with sf.SoundFile(self.audio_path, mode='x', samplerate=samplerate, channels=1) as file:
            with sd.InputStream(samplerate=samplerate, device=device, channels=1, callback=_callback):
                while self.recording:
                    file.write(q.get())

    def stop_recording(self):
        self.recording = False

    @staticmethod
    def get_sound_devices():
        return [device['name'] for device in sd.query_devices()]

