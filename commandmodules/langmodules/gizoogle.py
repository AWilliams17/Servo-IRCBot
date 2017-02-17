from bs4 import BeautifulSoup
from servomodules.ircformatting import changestyle, changecolor
import requests


def gizoogle(text):
    """
    Take a string and 'gizoogle' it, then returns the result.

    :param text: The string to be gizoogled.
    :return: If successful, then return the result.
    """
    URL = 'http://www.gizoogle.net/textilizer.php'

    html = requests.post(URL, data={'translatetext': text}).text
    try:
        gizoogledtext = str(BeautifulSoup(html, "html5lib").textarea.contents[0].strip())
    except (AttributeError, requests.ConnectionError):
        return changecolor("Failed to grab gizoogled text.", "red")
    except TypeError:
        return changecolor("Word must be a valid string.", "red")

    return gizoogledtext
