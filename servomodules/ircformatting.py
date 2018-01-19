# ToDo: Allow for the mixing of formats and colors(EG: A bold and red string).
# ToDo: Fix broken multi-line formatting/coloring
from enum import Enum


class ColorCodes(Enum):
    WHITE = "00"
    BLACK = "01"
    BLUE = "11"
    GREEN = "03"
    RED = "04"
    BROWN = "05"
    PURPLE = "06"
    ORANGE = "07"
    YELLOW = "08"
    LIGHT_GREEN = "09"
    TEAL = "10"
    GREY = "12"
    PINK = "13"


class StyleCodes(Enum):
    BOLD = "\x02"
    ITALIC = "\x1D"
    UNDERLINED = "\x1F"


def change_style(string, style_type):
    """
    Changes the style of an IRC string.
    :param string: The string to apply styling to.
    :param style_type: The value of the style you want. grab from StyleCodes.(style)
    :return: Returns the styled string.
    """
    return "%s%s%s" % (style_type.value, string, style_type.value)

def change_color(string, color):
    """
    Changes the color of an IRC string.
    :param string: The string to color.
    :param color: The value of the color you want. grab from ColorCodes.(color)
    :return: Returns the colored string.
    """
    return "%s%s%s%s" % ("\x03", color.value, string, "\x03")
