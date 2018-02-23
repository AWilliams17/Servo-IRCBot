from urllib import quote
from servomodules.ircformatting import change_style, change_color, ColorCodes, StyleCodes
import requests
import logging


def dictionary_define(word, def_num):
    """
    Grabs the definition of a word from the owlbot.info site.
    :param word: The word to be searched for.
    :param def_num: If multiple definitions are found, then this is the number indicating which to grab.
    :return: If a word doesn't exist, then it defaults to "Failed to grab definition." Otherwise, it returns
    the definition.
    """
    try:
        r = requests.get("https://owlbot.info/api/v1/dictionary/%s" % quote(word, safe=''))
        data = r.json()
        definition = data[int(def_num)].get("defenition")
        return "Got definition for %s: %s" % (change_style(str(word), StyleCodes.BOLD), str(definition))

    except (IndexError, requests.ConnectionError) as e:
        logging.error("Failed to grab Owl Dictionary definition for word %s, exception info: %r" % (word, e))
        return change_color("Failed to grab definition.", ColorCodes.RED)
    except TypeError:
        return change_color("Word must be a valid string.", ColorCodes.RED)
    except ValueError:
        return change_color("Definition number must be a valid int.", ColorCodes.RED)
