# ToDo: Add more tests for the formatting.
import pytest


@pytest.fixture(scope='module')
def command_handler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from servomodules.ircformatting import change_style, change_color
    command_handler = CommandHandler()

    @command_handler.register_command("!testcolor", "tests colored text")
    def test_color(string, color):
        return change_color(string, color)

    @command_handler.register_command("!teststyling", "tests styled text")
    def test_formatting(string, style):
        return change_style(string, style)

    return command_handler


@pytest.mark.usefixtures('command_handler_setup')
class TestIrcFormatting(object):

    def test_color_commands(self):
        with pytest.raises(Exception) as exc:
            assert command_handler_setup.serve("!testcolor test red") == "\x0304test\x03"
            assert command_handler_setup.serve("!testcolor test reagh") == exc
            assert command_handler_setup.serve("!testcolor test red") != exc

    def test_style_commands(self):
        with pytest.raises(Exception) as exc:
            assert command_handler_setup.serve("!teststyling test bold") == "\x02test\x02"
            assert command_handler_setup.serve("!teststyling test aegheah") == exc
            assert command_handler_setup.serve("!teststyling test bold") != exc
