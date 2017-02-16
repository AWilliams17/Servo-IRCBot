# ToDo: Add more tests for the formatting.
import pytest


@pytest.fixture(scope='module')
def commandhandler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from servomodules.ircformatting import changestyle, changecolor
    commandhandler = CommandHandler()

    @commandhandler.registercommand("!testcolor", "tests colored text")
    def test_color(string, color):
        return changecolor(string, color)

    @commandhandler.registercommand("!teststyling", "tests styled text")
    def test_formatting(string, style):
        return changestyle(string, style)

    return commandhandler


@pytest.mark.usefixtures('commandhandler_setup')
class Test_IrcFormatting(object):

    def test_colorcommands(self, commandhandler_setup):
        with pytest.raises(Exception) as exc:
            assert commandhandler_setup.serve("!testcolor test red") == "\x0304test\x03"
            assert commandhandler_setup.serve("!testcolor test reagh") == exc
            assert commandhandler_setup.serve("!testcolor test red") != exc

    def test_stylecommands(self, commandhandler_setup):
        with pytest.raises(Exception) as exc:
            assert commandhandler_setup.serve("!teststyling test bold") == "\x02test\x02"
            assert commandhandler_setup.serve("!teststyling test aegheah") == exc
            assert commandhandler_setup.serve("!teststyling test bold") != exc
