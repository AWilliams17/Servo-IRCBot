# Note: To use this module, you require an API key from DaybreakGames. Get one from https://census.daybreakgames.com/
#   and then put it in the whitespace following the s: in the continent_data variable.
from servomodules.ircformatting import change_style, change_color
import requests
import logging


def grab_continent_info(server_name, api_key):
    """
    Attempt to grab information pertaining to which faction has locked which continents on a given server.

    server_name is searched for in the server_ids, and if it is found, then the id of the server is retrieved,
    otherwise, an error message is returned notifying the user the server doesn't exist.

    api_key is the Daybreak games API key retrieved from the Servo.ini. If it's an invalid API key, then the
    function will just return its usual error message.

    :param server_name: The server to grab continent information from.
    :param api_key: The api key to be supplied to the api.
    :return: Upon success, a formatted string containing the locked/unlocked continents is returned. Otherwise,
    return an error message.
    """

    server_ids = {
        "Emerald": "17",
        "Connery": "1",
        "Briggs": "25",
        "Cobalt": "13",
        "Miller": "10"
    }

    faction_ids = {
        1: change_color("VS", "purple"),
        2: change_color("NC", "blue"),
        3: change_color("TR", "red")
    }

    continent_ids = {
        "Amerish": [6, 0, 1],
        "Esamir": [8, 28, 29],
        "Indar": [2, 9, 10],
        "Hossin": [4, 73, 74]
    }

    server = server_name[0].upper() + server_name[1:].lower()
    if server not in server_ids:
        return change_color("Invalid servername: %s" % server_name, "red")
    server_id = server_ids.get(server)

    def continent_statuses():
        """
        For the continents on the server, loop through each of them, getting the faction ids of the controlling
        faction of two warpgates. Then, in order to test if the continent is locked, compare the two warpgates
        against each other. If they are both owned by the same faction, then it's locked by that faction.

        Otherwise, it's unlocked.

        Either way, concatenate the status to the continent statuses list, and after looping through the
        continents, join the statuses into a string and return it.

        :return: Return the string that was concatenated from the continent statuses list.
        """
        continent_status_results = []

        for continent_name, continent_values in continent_ids.items():
            continent_data = requests.get(
                "http://census.daybreakgames.com/s:" + api_key + "/get/ps2:v2/map/?world_id=" + server_id + "&zone_ids=" +
                str(continent_values[0])).json()

            continent_map = continent_data['map_list'][0]['Regions']['Row']

            warpgate1_controlling_faction = continent_map[continent_values[1]]['RowData']['FactionId']
            warpgate2_controlling_faction = continent_map[continent_values[2]]['RowData']['FactionId']

            if warpgate1_controlling_faction != warpgate2_controlling_faction:
                continent_status_results.append("%s is unlocked" % change_style(continent_name, "bold"))
            else:
                continent_status_results.append("%s was locked by the %s" %
                                                (change_style(continent_name, "bold"),
                                                 faction_ids.get(int(warpgate1_controlling_faction))))

        continent_status_results.insert(3, "and")
        return ', '.join(continent_status_results).replace("and,", "and")

    try:
        return "On %s: %s." % (change_style(server, "bold"), continent_statuses())
    except (KeyError, requests.ConnectionError) as e:
        logging.error("Failed to return Planetside 2 continent info for server: %s. Exception: %r" % (server_name, e))
        return change_color("Could not retrieve continent information.", "red")
