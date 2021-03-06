from bs4 import BeautifulSoup
from servomodules.ircformatting import change_color, ColorCodes, StyleCodes
import logging
import requests


def gizoogle(text):
    """
    Take a string and 'gizoogle' it, then return the result.

    If the function fails to do so, then an error message is returned.

    :param text: The string to be gizoogled.
    :return: If successful, then return the result.
    """
    url = 'http://www.gizoogle.net/textilizer.php'

    html = requests.post(url, data={'translatetext': text}).text
    try:
        return str(BeautifulSoup(html, "html5lib").textarea.contents[0].strip())
    except (AttributeError, requests.ConnectionError) as e:
        logging.error("Failed to receive gizoogled text: %r" % e)
        return change_color("Failed to grab gizoogled text.", ColorCodes.RED)
    except TypeError:
        return change_color("Word must be a valid string.", ColorCodes.RED)
