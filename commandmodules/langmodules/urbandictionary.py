from urllib import quote
from servomodules.ircformatting import change_style, change_color
import requests
import logging


def define_word(word):
    """
    Attempt to grab the first definition of a given word from the Urban Dictionary site.
    :param word: The word to look up.
    :return: Upon success, return the definition of the word. If the definition was not found, the resulting
    index_error exception is caught and an error message is returned.
    """
    r = requests.get("http://api.urbandictionary.com/v0/define?term=%s)" % quote(word, safe=''))
    data = r.json()

    try:
        definition = data['list'][0]['definition']
        return "Got definition for %s: %s" % (change_style(str(word), "bold"), str(definition))
    except (IndexError, requests.ConnectionError) as e:
        logging.error("Failed to grab Urban Dictionary definition for word %s, exception info: %r" % (word, e))
        return change_color("Failed to grab definition.", "red")
    except TypeError:
        return change_color("Word must be a valid string.", "red")
