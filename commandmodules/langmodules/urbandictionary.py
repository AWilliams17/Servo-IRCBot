import requests
from urllib import quote
from servomodules.ircformatting import changestyle, changecolor


def defineword(word):
    """
    Attempt to grab the first definition of a given word from the Urban Dictionary site.

    :param word: The word to look up.
    :return: Upon success, return the definition of the word. If the definition was not found, an indexerror is raised.
    """
    r = requests.get("http://api.urbandictionary.com/v0/define?term=%s)" % quote(word, safe=''))
    data = r.json()

    try:
        definition = data['list'][0]['definition']
    except IndexError:
        return changecolor("Failed to grab definition.", "red")
    except TypeError:
        return changecolor("Word must be a valid string.", "red")

    return "Got definition for %s: %s" % (changestyle(str(word), "bold"), str(definition))
