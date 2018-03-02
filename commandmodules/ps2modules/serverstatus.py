from servomodules.ircformatting import change_style, change_color, StyleCodes, ColorCodes
from BeautifulSoup import BeautifulSoup
import requests
import logging

r = requests.get("http://www.planetside-universe.com/server_status.php").content
bs4 = BeautifulSoup(r).find('tbody', attrs={'id': 'server_status'})
result = bs4.text

server_ids = {
        "emerald": "17",
        "connery": "1",
        "briggs": "25",
        "cobalt": "13",
        "miller": "10"
    }


def grab_server_status(server_name):
    name_arg = str(server_name).lower()
    if name_arg not in server_ids:
        return change_color("Error: That server does not exist.", ColorCodes.RED)

    r = requests.get("http://www.planetside-universe.com/server_status.php")
    rp = requests.get("http://ps2.fisu.pw/api/population/?world=%s" % server_ids.get(name_arg))

    if rp.status_code != 200:
        logging.error("Error - Failed to grab population status. Status code: %s" % str(rp.status_code))
        return change_color("Error: Failed to retrieve population statistics.", ColorCodes.RED)

    if r.status_code != 200:
        logging.error("Error - Failed to grab population status. Status code: %s" % str(rp.status_code))
        return change_color("Error: Server returned %s" % r.status_code, ColorCodes.RED)

    rp = rp.json()

    vs_population = rp['result'][0]['vs']
    tr_population = rp['result'][0]['tr']
    nc_population = rp['result'][0]['nc']
    total_population = str(int(vs_population) + int(tr_population) + int(nc_population))

    rc = r.content

    data = []
    table = BeautifulSoup(rc).find('table', attrs={'id': 'servers'})
    table_body = table.find('tbody')

    for row in table_body.findAll("tr"):
        cells = row.findAll("td")
        cells = [ele.text.strip() for ele in cells]
        data.append([ele for ele in cells if ele])

    status = ""
    for i in data:
        if i[1] == name_arg.title():
            if i[3] != 'Up':
                status = "'%s' is down." % change_style(i[1], StyleCodes.BOLD)
            else:
                status = "%s is online with a total population of %s --- %s, %s, and %s." \
                         % (change_style(i[1], StyleCodes.BOLD),
                            change_color(total_population, ColorCodes.GREEN),
                            change_color(str(vs_population) + " VS", ColorCodes.PURPLE),
                            change_color(str(tr_population) + " TR", ColorCodes.RED),
                            change_color(str(nc_population) + " NC", ColorCodes.TEAL))

    return status
