import json
import queue
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import sounddevice as sd
import vosk

from app.core import dictionary
from app.core.config import settings
from app.core.logger import get_logger
from app.services.functions import *


q = queue.Queue() # Получаем частоту микрофона
logger = get_logger(__name__)


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    # Проверяем есть ли имя бота в data, если нет, то return
    trg = settings.TRIGGERS_NAMES.intersection(data.split())
    if not trg:
        return

    # Удаляем имя бота из текста
    data = data.replace(list(trg)[0], '')

    # Получаем вектор полученного текста
    # С равниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # Получение имени функции из ответа из data_set
    func_name = answer.split()[0]
    commands = {"passive": passive}
    commands.get(func_name, lambda: print("Unknown command"))()


def main():
    model = vosk.Model('ASR_MODEL')
    device = sd.default.device
    samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate']) 

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(dictionary.data_set.keys()))
    
    clf = LogisticRegression()
    clf.fit(vectors, list(dictionary.data_set.values()))

    del dictionary.data_set

    # Постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype='int16',
                                channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        logger.info("Система запущена и готова к распознаванию речи.")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)