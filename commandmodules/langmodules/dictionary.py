from urllib import quote
from servomodules.ircformatting import changestyle, changecolor
import requests
import logging

def dictionarydefine(word, defnum):

    try:
        r = requests.get("https://owlbot.info/api/v1/dictionary/%s" % quote(word, safe=''))
        data = r.json()
        definition = data[int(defnum)].get("defenition")
        return "Got definition for %s: %s" % (changestyle(str(word), "bold"), str(definition))

    except (IndexError, requests.ConnectionError) as e:
        logging.error("Failed to grab Owl Dictionary definition for word %s, exception info: %r" % (word, e))
        return changecolor("Failed to grab definition.", "red")
    except TypeError:
        return changecolor("Word must be a valid string.", "red")
    except ValueError:
        return changecolor("Definition number must be a valid int.", "red")
