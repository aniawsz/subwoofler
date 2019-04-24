import tkinter as tk

from queue import Queue

from getch import getch
from rompler import Rompler
from translations import KEYBOARD_KEY_TO_MIDI_NOTE


class Application(tk.Frame):
    def __init__(self, root, *a, **kw):
        super(Application, self).__init__(root, *a, **kw)

        # Set up the main window
        root.title("Subwoofler")
        root.geometry("600x400+400+150")
        root.config(bg="#ffffff")
        root.resizable(0,0)

        self._root = root
        self._notes_queue = Queue(maxsize=1)
        self._rompler = Rompler(name="AudioThread", notes_queue=self._notes_queue)
        self._rompler.start()

        # Stop the audio thread when the app is closing
        root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        self._rompler.stop.set()
        self._root.destroy()


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
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
