import numpy as np
import time
import wave

from threading import Event, Thread

from config import BUFFER_SIZE, SAMPLE_NAME
from player import Player
from sample import EmptySampleException, Sample
from translations import midi_note_to_speed


def lerp(left, right, fraction):
    """
    Interpolates linearly between two given points.
    Fraction is a number in the range [0, 1].
    """
    return (1 - fraction) * left + fraction * right


class Rompler(Thread):

    def __init__(self, notes_queue, *a, **k):
        super(Rompler, self).__init__(*a, **k)

        self._notes_queue = notes_queue
        self._note = None

        sample = Sample(*self._read_sample())
        if len(sample.data) <= 0:
            raise EmptySampleException
        self._sample = sample
        self._data_type = sample.data_type

        # Subtracting the last padding zero for interpolation (see the Sample class)
        self._max_position = len(sample.data) - 2
        self._current_position = 0.0

        self._zeros = np.zeros(BUFFER_SIZE, dtype=self._data_type)

        self._playback_speed = 1.0

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

    def _generate_next_sample_buffer(self):
        data = self._sample.data
        for _ in range(BUFFER_SIZE):
            position = self._current_position
            if position < self._max_position:
                sample_index = int(position)
                yield lerp(
                    data[sample_index],
                    data[sample_index + 1],
                    position - sample_index
                )
                self._current_position += self._playback_speed
            else:
                yield 0

    def _generate_next_buffer(self):
        # Check if a new note was added to the queue; if so, play the new note
        if not self._notes_queue.empty():
            self._note = self._notes_queue.get()
            self._current_position = 0.0
            self._playback_speed = midi_note_to_speed(self._note)

        if self._note:
            sample_buffer = np.fromiter(
                self._generate_next_sample_buffer(),
                dtype=self._data_type,
                count=BUFFER_SIZE
            )
            return sample_buffer
        return self._zeros

    def run(self):
        with self._player.stream_audio():
            while not self.stop.is_set():
                time.sleep(0.1)
