import numpy as np
import time
import wave

from threading import Event, Thread

from config import BUFFER_SIZE, SAMPLE_NAME
from player import Player
from sample import EmptySampleException, Sample


class Rompler(Thread):

    def __init__(self, *a, **k):
        super(Rompler, self).__init__(*a, **k)

        sample = Sample(*self._read_sample())
        if len(sample.data) <= 0:
            raise EmptySampleException
        self._sample = sample
        self._data_type = sample.data_type

        self._player = Player(
            generate_data_callback=self._generate_next_buffer,
            sample_width=sample.sample_width,
            number_of_channels=sample.number_of_channels,
            sample_rate=sample.sample_rate,
        )

        self.stop = Event()

    def _read_sample(self):
        with wave.open(SAMPLE_NAME, "rb") as f:
            fs = f.getframerate()
            channels_no = f.getnchannels()
            data = f.readframes(-1)
            sample_width = f.getsampwidth()
            return fs, channels_no, data, sample_width

    def _generate_next_buffer(self):
        return np.zeros(BUFFER_SIZE, dtype=self._data_type)

    def run(self):
        with self._player.stream_audio():
            while not self.stop.is_set():
                time.sleep(0.1)
