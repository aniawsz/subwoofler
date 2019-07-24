import tkFont

from .settings import Font


# Draws a rectangle with rounded corners on top of a tkinter.Canvas
def create_round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    r = radius
    points = (
        x1+r, y1, x1+r, y1,
        x2-r, y1, x2-r, y1,
        x2, y1, x2, y1+r,
        x2, y1+r, x2, y2-r,
        x2, y2-r, x2, y2,
        x2-r, y2, x2-r, y2,
        x1+r, y2, x1+r, y2,
        x1, y2, x1, y2-r,
        x1, y2-r, x1, y1+r,
        x1, y1+r, x1, y1)
    return canvas.create_polygon(points, smooth=True, **kwargs)


def make_font(family=Font.family, size=Font.size):
    return tkFont.Font(family=family, size=size)
