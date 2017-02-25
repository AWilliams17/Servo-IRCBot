# ToDo: Allow for the mixing of formats and colors(EG: A bold and red string).
# ToDo: Fix broken multi-line formatting/coloring
"""
The color_codes dictionary contained the proper IRC codes for coloring messages,
and likewise for style_codes, only for styles of the messages!
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
    """
    Attempt to take string and style, and then check if the style the user wants exists. If it does,
    then grab the code associated with the style, and then take the string and wrap it with the code,
    returning the result.

    :param string: The string that is to be styled.
    :param style: The desired style. If it doesn't exist, raise a ValueError.
    :return: Returns the formatted string if successful.
    """
    if style in style_codes:
        desired_style = style_codes.get(style)
        return "%s%s%s" % (desired_style, string, desired_style)
    else:
        raise ValueError("The style '%s' does not exist! Valid styles: %s" % (str(style), style_codes.keys()))


def changecolor(string, color):
    """
    Attemept to take a string and color, then check if the color the user wants exists. If it does,
    then grab the code associated with the color, and then take the string and wrap it with the code,
    returning the result.

    :param string: The string that is to be colored.
    :param color: The desired color. If it doesn't exist, raise a ValueError.
    :return: Returns a formatted string if successful.
    """
    if color in color_codes:
        desired_color = color_codes.get(color)
        return "%s%s%s%s" % ("\x03", desired_color, string, "\x03")
    else:
        raise ValueError("The color '%s' does not exist! Valid colors: %s" % (str(color), color_codes.keys()))
