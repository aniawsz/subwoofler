import sounddevice
import numpy as np

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

    def stream_audio(self):
        def callback(outdata, frames, time, status):
            data = self._generate_data()
            if data.ndim < 2: # bodge?
                data = data.reshape(-1, 1)
            outdata[:] = data

        def get_dtype_from_width(width):
            if width == 1:
                return np.uint8
            elif width == 2:
                return np.int16
            elif width == 4:
                return np.float32
            else:
                raise ValueError("Invalid width: %d" % width)

        return sounddevice.OutputStream(
            channels=self._number_of_channels,
            callback=callback,
            samplerate=self._sample_rate,
            dtype=get_dtype_from_width(self._sample_width),
            blocksize=BUFFER_SIZE
        )
