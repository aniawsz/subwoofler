from queue import Queue

from getch import getch
from rompler import Rompler
from translations import KEYBOARD_KEY_TO_MIDI_NOTE


def run():
    notes_queue = Queue(maxsize=1)
    rompler = Rompler(name="AudioThread", notes_queue=notes_queue)
    rompler.start()
    while True:
        char = getch()
        if (char == 'q'):
            print("quitting")
            rompler.stop.set()
            exit(0)
        else:
            print("pressed: ", char)
            try:
                midi_note = KEYBOARD_KEY_TO_MIDI_NOTE[char]
                notes_queue.put(midi_note)
            except KeyError:
                print("note not supported")


if __name__ == '__main__':
    run()
