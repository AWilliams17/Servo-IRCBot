from servomodules.ircformatting import change_style, change_color, StyleCodes, ColorCodes
import requests
from BeautifulSoup import BeautifulSoup
import logging

r = requests.get("http://www.planetside-universe.com/server_status.php").content
bs4 = BeautifulSoup(r).find('tbody', attrs={'id': 'server_status'})
result = bs4.text

server_names = ['emerald', 'connery', 'cobalt', 'miller', 'briggs']


def server_status(server_name):
    name_arg = str(server_name).lower()
    if name_arg not in server_names:
        return "err server not existerino"

    r = requests.get("http://www.planetside-universe.com/server_status.php")

    if r.status_code != 200:
        return "server returned %s" % r.status_code

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
                status = "The server '%s' is down." % i[1]
            else:
                status = "%s is %s with a %s population." % (i[1], str(i[3]).lower(), i[2])

    return status


if __name__ == '__main__':
    print server_status("Emerald")
