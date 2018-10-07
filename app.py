from getch import getch
from translations import KEYBOARD_KEY_TO_MIDI_NOTE


def run():
    while True:
        char = getch()
        if (char == 'q'):
            print("quitting")
            exit(0)
        else:
            print("pressed: ", char)
            try:
                midi_note = KEYBOARD_KEY_TO_MIDI_NOTE[char]
                print("midi note: ", midi_note)
            except KeyError:
                print("note not supported")


if __name__ == '__main__':
    run()
