# Note: To use this module, you require an API key from DaybreakGames. Get one from https://census.daybreakgames.com/
#   and then put it in the whitespace following the s: in the continentdata variable.
# ToDo: Refactor some of this mess.
import requests
from servomodules.ircformatting import changestyle, changecolor


def grabcontinentinfo(servername):
    """
    Attempt to grab information pertaining to which faction has locked which continents on a given server.

    :param servername: The server to grab continent information from.
    :return: Upon success, a formatted string containing the locked/unlocked continents is returned.
    """
    serverids_dict = {"emerald": ["Emerald", "17"],
                   "connery": ["Connery", "1"],
                   "briggs": ["Briggs", "25"],
                   "cobalt": ["Cobalt", "13"],
                   "miller": ["Miller", "10"]}

    factionids_dict = {1: changecolor("VS", "purple"),
                       2: changecolor("NC", "blue"),
                       3: changecolor("TR", "red")}

    continentids_dict = {"Amerish": [6, 0, 1],
                         "Esamir": [8, 28, 29],
                         "Indar": [2, 9, 10],
                         "Hossin": [4, 73, 74]}
    servernamel = servername.lower()
    try:
        server = serverids_dict.get(servernamel)[0]
        serverid = serverids_dict.get(servernamel)[1]
    except TypeError:
        return changecolor("Invalid servername: %s" % servername, "red")

    def continentstatuses():
        continent_statuses = []

        for continent_name, continent_values in continentids_dict.items():
            continentdata = requests.get(
                "http://census.daybreakgames.com/s: /get/ps2:v2/map/?world_id=" + serverid + "&zone_ids=" +
                str(continent_values[0])).json()
            continentmap = continentdata['map_list'][0]
            warpgate1_controlling_faction = continentmap['Regions']['Row'][continent_values[1]]['RowData']['FactionId']
            warpgate2_controlling_faction = continentmap['Regions']['Row'][continent_values[2]]['RowData']['FactionId']
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
    except (KeyError, requests.ConnectionError):
        return changecolor("Could not retrieve continent information.", "red")
