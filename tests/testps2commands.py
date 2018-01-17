# These are all going to fail mostly because the API key isn't included. :p
import pytest
from servomodules.ircformatting import change_color


@pytest.fixture(scope='module')
def command_handler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from commandmodules.ps2modules import grabstats, continentstatus
    command_handler = CommandHandler()

    @command_handler.register_command("!playerstats", "grabs a players stats")
    def ps2_player_stats(player):
        return grabstats.grab_player_stats(player, "a")

    @command_handler.register_command("!continentstatus", "grabs the continent info of a server")
    def ps2continent(server):
        return continentstatus.grab_continent_info(server, "a")

    return command_handler


@pytest.mark.usefixtures('command_handler_setup')
class TestPS2Commands(object):
    def test_player_stats(self):
        assert command_handler_setup.serve("!playerstats hiimnotreal") != \
            change_color("Could not retrieve player information.", "red")

        assert command_handler_setup.serve("!playerstats Mentis2k6") != \
            change_color("Could not retrieve player information.", "red")

        assert command_handler_setup.serve("!playerstats IHacksXVS") != \
            change_color("Could not retrieve player information.", "red")

    def test_continent_status(self):
        assert command_handler_setup.serve("!continentstatus emerald") != change_color("Invalid server name.", "red")
        assert command_handler_setup.serve("!continentstatus foo") == change_color("Invalid servername: foo", "red")
