import tkinter as tk

from queue import Queue

from rompler import Rompler
from translations import KEYBOARD_KEY_TO_MIDI_NOTE
from view import MainView


class Application(object):
    def __init__(self, window, *a, **kw):
        super(Application, self).__init__(*a, **kw)

        self._window = window

        # Create the app's GUI
        self._view = MainView(window)

        # Create and start an audio thread.
        # It's going to communicate with the main thread through a thread-safe queue.
        self._notes_queue = Queue(maxsize=1)
        self._rompler = Rompler(name="AudioThread", notes_queue=self._notes_queue)
        self._rompler.start()

        # Stop the audio thread when the app is closing
        window.protocol("WM_DELETE_WINDOW", self._on_closing)

        window.bind("<Key>", self._handle_keypress)

    def _on_closing(self):
        self._rompler.stop.set()
        self._window.destroy()

    def _handle_keypress(self, event):
        try:
            midi_note = KEYBOARD_KEY_TO_MIDI_NOTE[event.char]
            self._notes_queue.put(midi_note)
        except KeyError:
            print("note not supported")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
