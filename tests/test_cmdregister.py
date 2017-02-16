import pytest


@pytest.fixture(scope='module')
def commandhandler_setup(request):
    from servomodules.commandhandler import CommandHandler
    commandhandler = CommandHandler()

    @commandhandler.registercommand("!cmd1")
    def cmd1():
        return "This is cmd1. It has no arguments."

    @commandhandler.registercommand("!cmd2", "cmd2 has a description")
    def cmd2():
        return "This is cmd2. It has no arguments, but it has a description."

    @commandhandler.registercommand("!cmd3")
    def cmd3(onearg):
        return "This is cmd3. It has one argument: %s" % onearg

    @commandhandler.registercommand("!cmd4", "cmd4 has a description and a single argument.")
    def cmd4(onearg):
        return "This is cmd4. It has one argument: %s and a description." % onearg

    @commandhandler.registercommand("!cmd5")
    def cmd5(onearg, twoarg):
        return "This is cmd5. It has two arguments: %s and %s" % onearg, twoarg

    @commandhandler.registercommand("!cmd6", "cmd6 has a description and two arguments.")
    def cmd6(onearg, twoarg):
        return "This is cmd6. It has two arguments: %s and %s and a description." % onearg, twoarg

    @commandhandler.registercommand("!cmd7")
    def cmd7(*args):
        return "This is cmd7. It has variable arguments: %s" % args

    @commandhandler.registercommand("!cmd8", "cmd8 has a description and variable arguments.")
    def cmd8(*args):
        return "This is cmd8. It has variable arguments: %s and a description." % args

    @commandhandler.registercommand("!samecommand", "This is samecommand.")
    def same():
        return "Same command 1 was called."

    @commandhandler.registercommand("!samecommand", "This is also samecommand.")
    def same2():
        return "Same command 2 was called."

    @commandhandler.registercommand("!samecommand", "This is samecommand as well. And it shares the same function.")
    def same():
        return "This is the duplicate same function."

    with pytest.raises(ValueError) as excinfo:
        @commandhandler.registercommand("")
        def emptycmd():
            return "This is an empty command."
    assert excinfo.value.message == "Can't define a command with no command string"

    return commandhandler


@pytest.mark.usefixtures('commandhandler_setup')
class Test_CmdRegister(object):

    def test_samecmd(self, commandhandler_setup):
        assert commandhandler_setup.serve("!samecommand") == "This is the duplicate same function."

    def test_emptycmd(self, commandhandler_setup):
        assert commandhandler_setup.serve("") is None
