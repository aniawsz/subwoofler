import wave

from config import SAMPLE_NAME
from sample import EmptySampleException, Sample


class Rompler(object):

    def __init__(self, *a, **k):
        sample = Sample(*self._read_sample())
        if len(sample.data) <= 0:
            raise EmptySampleException
        self._sample = sample

    def _read_sample(self):
        with wave.open(SAMPLE_NAME, "rb") as f:
            fs = f.getframerate()
            channels_no = f.getnchannels()
            data = f.readframes(-1)
            sample_width = f.getsampwidth()
            return fs, channels_no, data, sample_width

