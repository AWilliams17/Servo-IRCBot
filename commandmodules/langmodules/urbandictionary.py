from urllib import quote
from servomodules.ircformatting import changestyle, changecolor
import requests
import logging


def defineword(word):
    """
    Attempt to grab the first definition of a given word from the Urban Dictionary site.
    :param word: The word to look up.
    :return: Upon success, return the definition of the word. If the definition was not found, the resulting
    indexerror exception is caught and an error message is returned.
    """
    r = requests.get("http://api.urbandictionary.com/v0/define?term=%s)" % quote(word, safe=''))
    data = r.json()

    try:
        definition = data['list'][0]['definition']
        return "Got definition for %s: %s" % (changestyle(str(word), "bold"), str(definition))
    except (IndexError, requests.ConnectionError) as e:
        logging.error("Failed to grab Urban Dictionary definition for word %s, exception info: %r" % (word, e))
        return changecolor("Failed to grab definition.", "red")
    except TypeError:
        return changecolor("Word must be a valid string.", "red")
