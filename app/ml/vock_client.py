import json
import vosk
from app.core.logger import get_logger

logger = get_logger(__name__, "logs.log")


class VoskModel:
    def __init__(self, model_name: str = "ASR_MODEL", samplerate: int = 16000):
        self.model = vosk.Model(model_name)
        self.rec = vosk.KaldiRecognizer(self.model, samplerate)
        logger.debug(f"Vosk-модель успешно загружена")

    def recognize(self, data: bytes):
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())['text']
            return result
        else:
            return None