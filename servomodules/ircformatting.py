# ToDo: Allow for the mixing of formats and colors(EG: A bold and red string).
# ToDo: Fix broken multi-line formatting/coloring
"""
This module contains functions which take a string, and then either changes the color of the string, or the format
of the string, and returns the result.
"""
color_codes = {
    "white": "00", "black": "01", "blue": "11",
    "green": "03", "red": "04", "brown": "05",
    "purple": "06", "orange": "07", "yellow": "08",
    "lightgreen": "09", "teal": "10", "grey": "12",
    "pink": "13"
}

style_codes = {
    "bold": "\x02", "italic": "\x1D",
    "underlined": "\x1F"
}


def changestyle(string, style):
    if style in style_codes:
        desired_style = style_codes.get(style)
        return "%s%s%s" % (desired_style, string, desired_style)
    else:
        raise ValueError("The style '%s' does not exist! Valid styles: %s" % (str(style), style_codes.keys()))


def changecolor(string, color):
    if color in color_codes:
        desired_color = color_codes.get(color)
        return "%s%s%s%s" % ("\x03", desired_color, string, "\x03")
    else:
        raise ValueError("The color '%s' does not exist! Valid colors: %s" % (str(color), color_codes.keys()))
