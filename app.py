import Tkinter as tk

from Queue import Queue

from rompler import Rompler
from translations import KEYBOARD_KEY_TO_MIDI_NOTE
from views.main_view import MainView


class Application(object):
    def __init__(self, window, *a, **kw):
        super(Application, self).__init__(*a, **kw)

        self._window = window

        # Create and start an audio thread.
        # It's going to communicate with the main thread through a thread-safe queue.
        self._notes_queue = Queue(maxsize=1)
        self._rompler = Rompler(name="AudioThread", notes_queue=self._notes_queue)
        self._rompler.start()

        # Create the app's GUI
        self._view = MainView(window, self._rompler)

        # Stop the audio thread when the app is closing
        window.protocol("WM_DELETE_WINDOW", self._on_closing)

        window.bind("<Key>", self._handle_keypress)
        window.bind("<KeyRelease>", self._handle_keyrelease)

    def _on_closing(self):
        self._rompler.stop.set()
        self._window.destroy()

    def _handle_keypress(self, event):
        try:
            key = event.char
            midi_note = KEYBOARD_KEY_TO_MIDI_NOTE[key]
            self._notes_queue.put(midi_note)
            self._view.on_key_pressed(key)
        except KeyError:
            # note not supported
            pass

    def _handle_keyrelease(self, event):
        key = event.char
        self._view.on_key_released(key)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.attributes("-topmost", True)
    root.mainloop()
