import pytest


@pytest.fixture(scope='module')
def command_handler_setup(request):
    from servomodules.commandhandler import CommandHandler
    command_handler = CommandHandler()

    @command_handler.register_command("!cmd1")
    def cmd1():
        return "This is cmd1. It has no arguments."

    @command_handler.register_command("!cmd2", "cmd2 has a description")
    def cmd2():
        return "This is cmd2. It has no arguments, but it has a description."

    @command_handler.register_command("!cmd3")
    def cmd3(one_arg):
        return "This is cmd3. It has one argument: %s" % one_arg

    @command_handler.register_command("!cmd4", "cmd4 has a description and a single argument.")
    def cmd4(one_arg):
        return "This is cmd4. It has one argument: %s and a description." % one_arg

    @command_handler.register_command("!cmd5")
    def cmd5(one_arg, two_arg):
        return "This is cmd5. It has two arguments: %s and %s" % one_arg, two_arg

    @command_handler.register_command("!cmd6", "cmd6 has a description and two arguments.")
    def cmd6(one_arg, two_arg):
        return "This is cmd6. It has two arguments: %s and %s and a description." % one_arg, two_arg

    @command_handler.register_command("!cmd7")
    def cmd7(*args):
        return "This is cmd7. It has variable arguments: %s" % args

    @command_handler.register_command("!cmd8", "cmd8 has a description and variable arguments.")
    def cmd8(*args):
        return "This is cmd8. It has variable arguments: %s and a description." % args

    @command_handler.register_command("!samecommand", "This is samecommand.")
    def same():
        return "Same command 1 was called."

    @command_handler.register_command("!samecommand", "This is also samecommand.")
    def same2():
        return "Same command 2 was called."

    @command_handler.register_command("!samecommand", "This is samecommand as well. And it shares the same function.")
    def same():
        return "This is the duplicate same function."

    with pytest.raises(ValueError) as excinfo:
        @command_handler.register_command("")
        def empty_cmd():
            return "This is an empty command."
    assert excinfo.value.message == "Can't define a command with no command string"

    return command_handler


@pytest.mark.usefixtures('command_handler_setup')
class TestCommandRegister(object):

    def test_same_command(self):
        assert command_handler_setup.serve("!samecommand") == "This is the duplicate same function."

    def test_empty_command(self):
        assert command_handler_setup.serve("") is None
