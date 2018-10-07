import numpy as np


SAMPLE_WIDTH_TO_NP_DATA_TYPE = {
    1: np.int8,
    2: np.int16,
    4: np.int32,
}


class EmptySampleException(Exception):
    def __str__(self):
        return "Please provide a non-empty sample"


class UnsupportedSampleWidth(Exception):
    def __str__(self):
        return "Can't read the sample because of unsupported sample width"


class Sample(object):
    """A read-only container for sample data"""
    def __init__(self, fs, channels_no, raw_data, sample_width):
        self._fs = fs
        self._channels_no = channels_no

        # An array with frames of audio sample data.
        # A frame size depends on the number of channels and
        # the with of an audio sample in bytes:
        #   frame_size = channels_no * sample_width
        try:
            self._data_type = SAMPLE_WIDTH_TO_NP_DATA_TYPE[sample_width]
        except KeyError:
            raise UnsupportedSampleWidth()
        self._data = np.fromstring(raw_data, self._data_type)

        self._sample_width = sample_width

    @property
    def sample_rate(self):
        """Sample rate in Hz"""
        return self._fs

    @property
    def number_of_channels(self):
        """Number of audio channels. Returns 1 for mono, 2 for stereo"""
        return self._channels_no

    @property
    def data(self):
        """A numpy array of frames of audio data"""
        return self._data

    @property
    def sample_width(self):
        """Sample width in bytes"""
        return self._sample_width

    @property
    def data_type(self):
        """Numpy data type of the stored sample data"""
        return self._data_type
