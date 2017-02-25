# Note: To use this module, you require an API key from DaybreakGames. Get one from https://census.daybreakgames.com/
#   and then put it in the whitespace following the s: in the data variable.
from __future__ import division
from servomodules.ircformatting import changestyle, changecolor
import requests
import logging


def grabplayerstats(playername, apikey):
    """
    Attempt to grab a specified player's battlerank, faction, certs, kill/death count and KDR.

    :param playername: This is the player to search for. If the player is not found, then this usually results in an
    indexerror/keyerror. ZeroDivisionErrors occur when a player is outdated and has no kills/deaths in the census db.

    :return: Return a formatted string containing the discovered information.

    """

    factionids_dict = {1: "VS",
                       2: "NC",
                       3: "TR"}
    try:
        data = requests.get("http://census.daybreakgames.com/s:" + apikey + "/get/ps2:v2/character/?name.first_lower=" +
                            playername.lower() + "&c:resolve=stat_history&c:resolve=world&c:join=world^on:world_id^to:"
                                                 "world_id^inject_at:world_id").json()
        censuschar = data['character_list'][0]
        charbr = str(censuschar['battle_rank']['value'])
        charfaction = str(factionids_dict.get(int(censuschar['faction_id'][0])))
        charcerts = str(censuschar['certs']['available_points'])
        charkills = str(censuschar['stats']['stat_history'][5]['all_time'])
        chardeaths = str(censuschar['stats']['stat_history'][2]['all_time'])
        charkd = round(int(charkills)/int(chardeaths), 2)
        return "Got stats for %s - battlerank: %s, faction: %s, certcount: %s, kills: %s, deaths: %s, KD: %s" % \
               (changestyle(playername, "bold"), charbr, charfaction, charcerts,
                charkills, chardeaths, charkd)
    except (IndexError, ZeroDivisionError, KeyError, requests.ConnectionError) as e:
        logging.error("Failed to grab Planetside 2 player %s's info. Exception info: %r" % (playername, e))
        return changecolor("Could not retrieve player information.", "red")
