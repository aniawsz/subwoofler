import pyaudio

from contextlib import contextmanager

from config import BUFFER_SIZE


class Player(object):

    def __init__(
        self,
        generate_data_callback,
        sample_width,
        number_of_channels,
        sample_rate,
        *a,
        **k
    ):
        self._generate_data = generate_data_callback
        self._sample_width = sample_width
        self._number_of_channels = number_of_channels
        self._sample_rate = sample_rate

    def _get_next_buffer(self, in_data, frame_count, time_info, status):
        return (self._generate_data(), pyaudio.paContinue)

    @contextmanager
    def stream_audio(self):
        pya = pyaudio.PyAudio()
        audio_stream = pya.open(
            format=pyaudio.get_format_from_width(self._sample_width),
            channels=self._number_of_channels,
            rate=self._sample_rate,
            output=True,
            stream_callback=self._get_next_buffer,
            frames_per_buffer=BUFFER_SIZE,
        )
        audio_stream.start_stream()
        try:
            yield audio_stream
        finally:
            audio_stream.stop_stream()
            audio_stream.close()
            pya.terminate()
