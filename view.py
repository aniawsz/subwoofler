import tkinter as tk


class MainView(tk.Frame):
    def __init__(self, window, *a, **kw):
        super(MainView, self).__init__(window, *a, **kw)

        self._window = window

        # Set up the main window
        window.title("Subwoofler")
        window.geometry("760x720+360+46")
        window.config(bg="#ffffff")
        window.resizable(0,0)

        self._keyboard_image = self._create_keyboard_image()

    def _create_keyboard_image(self):
        keyboard_image = tk.PhotoImage(file="images/keyboard.ppm")

        keyboard_canvas = tk.Canvas(
            self._window,
            width=keyboard_image.width(),
            height=keyboard_image.height(),
        )
        keyboard_canvas.pack()
        keyboard_canvas.create_image(0, 0, anchor=tk.NW, image=keyboard_image)

        return keyboard_image
