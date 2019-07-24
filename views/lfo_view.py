import Tkinter as tk

from .elements import SquareElement
from .helpers import create_round_rectangle
from .settings import ColorScheme


class Layout(object):
    on_off_button_begin_x = 176
    on_off_button_begin_y = 400

    rate_slider_begin_x = 240
    rate_slider_begin_y = 410


class ButtonOnItem(SquareElement):
    fill_color = ColorScheme.slate
    active_color = ColorScheme.red


class RateSliderItem(object):
    width = 18
    length = 111
    radius = ButtonOnItem.radius
    fill_color = ColorScheme.slate


class LfoView(object):
    def __init__(self, canvas, lfo, *a, **k):
        super(LfoView, self).__init__(*a, **k)

        self._canvas = canvas
        self._lfo = lfo

        self._set_up_on_off_button()
        self._set_up_rate_slider()

    def _set_up_on_off_button(self):
        self._on_off_button_id = self._create_on_off_button()

        side_width = ButtonOnItem.side_width
        self._on_off_button_frame = tk.Frame(
            None,
            width=side_width,
            height=side_width,
            background="",
        )
        self._on_off_button_frame.bind("<Button-1>", self._on_on_off_button_pressed)
        self._on_off_button_window = self._create_on_off_button_window()

    def _create_on_off_button(self):
        side_width = ButtonOnItem.side_width
        begin_x = Layout.on_off_button_begin_x
        begin_y = Layout.on_off_button_begin_y

        return create_round_rectangle(
            self._canvas,
            begin_x,
            begin_y,
            begin_x + side_width,
            begin_y + side_width,
            radius=ButtonOnItem.radius,
            fill=ButtonOnItem.active_color if self._lfo.is_on else ButtonOnItem.fill_color,
        )

    def _create_on_off_button_window(self):
        return self._canvas.create_window(
            Layout.on_off_button_begin_x,
            Layout.on_off_button_begin_y,
            anchor=tk.NW,
            window=self._on_off_button_frame,
        )

    def _on_on_off_button_pressed(self, event):
        self._lfo.is_on = not self._lfo.is_on
        self._canvas.itemconfig(
            self._on_off_button_id,
            fill=ButtonOnItem.active_color if self._lfo.is_on else ButtonOnItem.fill_color,
        )
        self._canvas.delete(self._on_off_button_window)
        self._on_off_button_window = self._create_on_off_button_window()

    def _set_up_rate_slider(self):
        self._rate_slider = self._create_rate_slider()

        self._canvas.create_window(
            Layout.rate_slider_begin_x + int(RateSliderItem.radius / 2),
            Layout.rate_slider_begin_y,
            anchor=tk.NW,
            window=self._rate_slider,
        )

    def _create_rate_slider(self):
        begin_x = Layout.rate_slider_begin_x
        begin_y = Layout.rate_slider_begin_y

        create_round_rectangle(
            self._canvas,
            begin_x,
            begin_y,
            begin_x + RateSliderItem.length,
            begin_y + RateSliderItem.width,
            radius=RateSliderItem.radius,
            fill=RateSliderItem.fill_color,
        )

        return tk.Scale(
            None,
            from_=0.5,
            to=15.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            background=ColorScheme.navy,
            activebackground=ColorScheme.light_gray,
            borderwidth=0,
            troughcolor=RateSliderItem.fill_color,
            showvalue=0,
            sliderlength=5,
            width=RateSliderItem.width,
            length=RateSliderItem.length - RateSliderItem.radius,
            command=self._set_lfo_rate,
        )

    def _set_lfo_rate(self, value):
        self._lfo.rate = float(value)
