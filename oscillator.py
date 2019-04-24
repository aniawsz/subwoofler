import numpy as np


class LFO(object):
    """
    Low frequency oscillator.
    Generates sine waves of specified rate and sampling frequency (in Hz).
    """
    def __init__(self, rate, sample_rate):
        self._rate = rate
        self._sample_rate = sample_rate
        self._is_on = False

        # Indicate the current position in the waveform cycle
        self._phase = 0.0
        self._update_phase_increment()

    def _update_phase_increment(self):
        self._phase_increment =  2 * np.pi * self._rate / self._sample_rate

    @property
    def is_on(self):
        return self._is_on

    @is_on.setter
    def is_on(self, value):
        self._is_on = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value
        self._update_phase_increment()

    @property
    def sample_rate(self):
        return self._rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value
        self._update_phase_increment()

    def generate_next_buffer(self, buffer_size=1):
        """
        Return buffer_size number of waveform points,
        starting where the last call left off.
        """
        for _ in range(buffer_size):
            phase = self._phase
            yield np.sin(phase)
            phase += self._phase_increment
            self._phase = phase

    def reset(self):
        self._phase = 0.0
