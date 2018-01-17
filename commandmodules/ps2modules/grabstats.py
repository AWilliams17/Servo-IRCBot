# Note: To use this module, you require an API key from DaybreakGames. Get one from https://census.daybreakgames.com/
#   and then put it in the whitespace following the s: in the data variable.
from __future__ import division
from servomodules.ircformatting import change_style, change_color
import requests
import logging


def grab_player_stats(player_name, api_key):
    """
    Attempt to grab a specified player's battlerank, faction, certs, kill/death count and KDR.

    The api key is retrieved from the Servo.ini file. If it is invalid, then the function simply
    returns its usual error message.

    :param player_name: This is the player to search for. If the player is not found, then this usually results in an
    indexerror/keyerror. ZeroDivisionErrors occur when a player is outdated and has no kills/deaths in the census db.

    :return: Return a formatted string containing the discovered information.

    """

    factionids_dict = {1: "VS",
                       2: "NC",
                       3: "TR"}
    try:
        data = requests.get("http://census.daybreakgames.com/s:" + api_key + "/get/ps2:v2/character/?name.first_lower=" +
                            player_name.lower() + "&c:resolve=stat_history&c:resolve=world&c:join=world^on:world_id^to:"
                                                 "world_id^inject_at:world_id").json()
        census_char = data['character_list'][0]
        char_br = str(census_char['battle_rank']['value'])
        char_faction = str(factionids_dict.get(int(census_char['faction_id'][0])))
        char_certs = str(census_char['certs']['available_points'])
        char_kills = str(census_char['stats']['stat_history'][5]['all_time'])
        char_deaths = str(census_char['stats']['stat_history'][2]['all_time'])
        char_kd = round(int(char_kills)/int(char_deaths), 2)
        return "Got stats for %s - battlerank: %s, faction: %s, certcount: %s, kills: %s, deaths: %s, KD: %s" % \
               (change_style(player_name, "bold"), char_br, char_faction, char_certs,
                char_kills, char_deaths, char_kd)
    except (IndexError, ZeroDivisionError, KeyError, requests.ConnectionError) as e:
        logging.error("Failed to grab Planetside 2 player %s's info. Exception info: %r" % (player_name, e))
        return change_color("Could not retrieve player information.", "red")
