import abc


class Engine(abc.ABC):

    END_VAL = "<END>"

    @abc.abstractmethod
    def recognize(self, audio_path, settings, result_callback):
        pass
