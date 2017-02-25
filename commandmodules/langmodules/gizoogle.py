from bs4 import BeautifulSoup
from servomodules.ircformatting import changecolor
import logging
import requests


def gizoogle(text):
    """
    Take a string and 'gizoogle' it, then returns the result.

    :param text: The string to be gizoogled.
    :return: If successful, then return the result.
    """
    url = 'http://www.gizoogle.net/textilizer.php'

    html = requests.post(url, data={'translatetext': text}).text
    try:
        return str(BeautifulSoup(html, "html5lib").textarea.contents[0].strip())
    except (AttributeError, requests.ConnectionError) as e:
        logging.error("Failed to receive gizoogled text: %r" % e)
        return changecolor("Failed to grab gizoogled text.", "red")
    except TypeError:
        return changecolor("Word must be a valid string.", "red")
