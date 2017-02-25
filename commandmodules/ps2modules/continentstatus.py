# Note: To use this module, you require an API key from DaybreakGames. Get one from https://census.daybreakgames.com/
#   and then put it in the whitespace following the s: in the continentdata variable.
# ToDo: Refactor some of this mess.
from servomodules.ircformatting import changestyle, changecolor
import requests
import logging


def grabcontinentinfo(servername, apikey):
    """
    Attempt to grab information pertaining to which faction has locked which continents on a given server.

    servername is searched for in the serverids_dict, and if it is found, then the id of the server is retrieved,
    otherwise, an error message is returned notifying the user the server doesn't exist.

    apikey is the Daybreak games API key retrieved from the Servo.ini. If it's an invalid API key, then the
    function will just return its usual error message.

    :param servername: The server to grab continent information from.
    :return: Upon success, a formatted string containing the locked/unlocked continents is returned. Otherwise,
    return an error message.
    """

    serverids_dict = {
        "Emerald": "17",
        "Connery": "1",
        "Briggs": "25",
        "Cobalt": "13",
        "Miller": "10"
    }

    factionids_dict = {
        1: changecolor("VS", "purple"),
        2: changecolor("NC", "blue"),
        3: changecolor("TR", "red")
    }

    continentids_dict = {
        "Amerish": [6, 0, 1],
        "Esamir": [8, 28, 29],
        "Indar": [2, 9, 10],
        "Hossin": [4, 73, 74]
    }

    server = servername[0].upper() + servername[1:].lower()
    if server not in serverids_dict:
        return changecolor("Invalid servername: %s" % servername, "red")
    serverid = serverids_dict.get(server)

    def continentstatuses():
        """
        For the continents on the server, loop through each of them, getting the faction ids of the controlling
        faction of two warpgates. Then, in order to test if the continent is locked, compare the two warpgates
        against each other. If they are both owned by the same faction, then it's locked by that faction.

        Otherwise, it's unlocked.

        Either way, concatenate the status to the continent statuses list, and after looping through the
        continents, join the statuses into a string and return it.

        :return: Return the string that was concatenated from the continent statuses list.
        """
        continent_statuses = []

        for continent_name, continent_values in continentids_dict.items():
            continentdata = requests.get(
                "http://census.daybreakgames.com/s:" + apikey + "/get/ps2:v2/map/?world_id=" + serverid + "&zone_ids=" +
                str(continent_values[0])).json()

            continentmap = continentdata['map_list'][0]['Regions']['Row']

            warpgate1_controlling_faction = continentmap[continent_values[1]]['RowData']['FactionId']
            warpgate2_controlling_faction = continentmap[continent_values[2]]['RowData']['FactionId']

            if warpgate1_controlling_faction != warpgate2_controlling_faction:
                continent_statuses.append("%s is unlocked" % changestyle(continent_name, "bold"))
            else:
                continent_statuses.append("%s was locked by the %s" %
                                          (changestyle(continent_name, "bold"),
                                           factionids_dict.get(int(warpgate1_controlling_faction))))

        continent_statuses.insert(3, "and")
        return ', '.join(continent_statuses).replace("and,", "and")

    try:
        return "On %s: %s." % (changestyle(server, "bold"), continentstatuses())
    except (KeyError, requests.ConnectionError) as e:
        logging.error("Failed to return Planetside 2 continent info for server: %s. Exception: %r" % (servername, e))
        return changecolor("Could not retrieve continent information.", "red")
