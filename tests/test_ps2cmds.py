# These are all going to fail mostly because the API key isn't included. :p
import pytest
from servomodules.ircformatting import changecolor, changestyle


@pytest.fixture(scope='module')
def commandhandler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from commandmodules.ps2modules import grabstats, continentstatus
    commandhandler = CommandHandler()

    @commandhandler.registercommand("!playerstats", "grabs a players stats")
    def ps2player(player):
        return grabstats.grabplayerstats(player, "a")

    @commandhandler.registercommand("!continentstatus", "grabs the continent info of a server")
    def ps2continent(server):
        return continentstatus.grabcontinentinfo(server, "a")

    return commandhandler


@pytest.mark.usefixtures('commandhandler_setup')
class Test_PS2Cmds(object):

    def test_playerstats(self, commandhandler_setup):
        assert commandhandler_setup.serve("!playerstats hiimnotreal") != \
               changecolor("Could not retrieve player information.", "red")

        assert commandhandler_setup.serve("!playerstats Mentis2k6") != \
               changecolor("Could not retrieve player information.", "red")

        assert commandhandler_setup.serve("!playerstats IHacksXVS") != \
               changecolor("Could not retrieve player information.", "red")

    def test_continentstatus(self, commandhandler_setup):
        assert commandhandler_setup.serve("!continentstatus emerald") != changecolor("Invalid server name.", "red")
        assert commandhandler_setup.serve("!continentstatus foo") == changecolor("Invalid servername: foo", "red")
