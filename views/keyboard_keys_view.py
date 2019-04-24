import tkinter as tk

from .elements import SquareElement
from .helpers import create_round_rectangle, make_font
from .settings import ColorScheme


class Layout(object):

    left_black_keys_begin_x = 240
    right_black_keys_begin_x = 440
    black_keys_begin_y = 503

    white_keys_begin_x = 201
    white_keys_begin_y = 661

    white_piano_key_width = 57
    white_piano_keys_spacing = 9

    black_piano_key_width = 45
    black_piano_keys_spacing = 21


class KeyboardKeyItem(SquareElement):
    fill_color = ColorScheme.light_gray
    active_color = ColorScheme.red
    font_color = ColorScheme.navy
    font_size = 16


LEFT_BLACK_KEYS = ['w', 'e']
RIGHT_BLACK_KEYS = ['t', 'y', 'u']
WHITE_KEYS = ['a', 's', 'd', 'f', 'g', 'h', 'j']


class KeyboardKeysView(object):
    def __init__(self, canvas, *a, **k):
        super(KeyboardKeysView, self).__init__(*a, **k)

        self._canvas = canvas

        self._keyboard_key_items = self._create_keyboard_key_items()

    def on_key_pressed(self, key):
        try:
            item_id = self._keyboard_key_items[key]
            self._canvas.itemconfig(item_id, fill=KeyboardKeyItem.active_color)
        except KeyError:
            pass

    def on_key_released(self, key):
        try:
            item_id = self._keyboard_key_items[key]
            self._canvas.itemconfig(item_id, fill=KeyboardKeyItem.fill_color)
        except KeyError:
            pass

    def _create_keyboard_key_items(self):
        keyboard_key_items = {}

        font = make_font(size=KeyboardKeyItem.font_size)

        width = KeyboardKeyItem.side_width

        white_keys_margin = Layout.white_piano_key_width - width
        spacing = Layout.white_piano_key_width + Layout.white_piano_keys_spacing

        keyboard_key_items.update(
            self._create_keyboard_key_items_for_keys(
                WHITE_KEYS,
                Layout.white_keys_begin_x,
                Layout.white_keys_begin_y,
                spacing,
                white_keys_margin,
                font,
            )
        )

        left_black_keys_margin = Layout.black_piano_key_width - width
        spacing = Layout.black_piano_key_width + Layout.black_piano_keys_spacing

        keyboard_key_items.update(
            self._create_keyboard_key_items_for_keys(
                LEFT_BLACK_KEYS,
                Layout.left_black_keys_begin_x,
                Layout.black_keys_begin_y,
                spacing,
                left_black_keys_margin,
                font,
            )
        )

        keyboard_key_items.update(
            self._create_keyboard_key_items_for_keys(
                RIGHT_BLACK_KEYS,
                Layout.right_black_keys_begin_x,
                Layout.black_keys_begin_y,
                spacing,
                left_black_keys_margin,
                font,
            )
        )

        return keyboard_key_items

    def _create_keyboard_key_items_for_keys(
        self,
        keys,
        begin_x,
        begin_y,
        spacing,
        margin,
        font
    ):
        keyboard_key_items = {}

        width = KeyboardKeyItem.side_width

        even_margins = margin % 2 == 0
        margin_left = int(margin / 2)
        begin_x += margin_left

        font_size = KeyboardKeyItem.font_size
        letter_width = font.metrics()['linespace']

        text_margin_left = int(width / 2 - letter_width / 2) + 4
        text_margin_top = int(width / 2 - font_size / 2)

        for ix, key in enumerate(keys):
            keyboard_key_items[key] = create_round_rectangle(
                self._canvas,
                begin_x,
                begin_y,
                begin_x + width,
                begin_y + width,
                radius=KeyboardKeyItem.radius,
                fill=KeyboardKeyItem.fill_color,
            )

            self._canvas.create_text(
                begin_x + text_margin_left,
                begin_y + text_margin_top,
                text=key.upper(),
                width=width,
                anchor=tk.NW,
                font=font,
                fill=KeyboardKeyItem.font_color,
            )

            begin_x += spacing

            # Compensate for uneven left and right margins to avoid drifting to the left
            if not even_margins and ix % 2 == 0:
                begin_x += 1

        return keyboard_key_items
