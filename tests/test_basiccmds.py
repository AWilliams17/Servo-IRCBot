import pytest


@pytest.fixture(scope='module')
def commandhandler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from commandmodules.testmodules import multiargadd, add2, sayhi
    commandhandler = CommandHandler()

    @commandhandler.registercommand("!add2", "adds 2 to given parameter")
    def add2cmd(num):
        return add2.add2toin(num)

    @commandhandler.registercommand("!multiargadd", "adds multiple args")
    def multiargaddcmd(num1, num2, num3):
        return multiargadd.add_multiargs(num1, num2, num3)

    @commandhandler.registercommand("!sayhi", "says hi to you :D", "multi string")
    def sayhicmd(name):
        return sayhi.sayhitoname(name)

    return commandhandler


@pytest.mark.usefixtures('commandhandler_setup')
class Test_BasicCmds(object):

    def test_add2(self, commandhandler_setup):  # Tests for single argument commands.
        assert commandhandler_setup.serve("!add2 4") == 6
        assert commandhandler_setup.serve("!add2 2") != 3
        assert commandhandler_setup.serve("!add2 2 2") == "Too many parameters (2 given, 1 needed)"
        assert commandhandler_setup.serve("!add2 not a number") == "Too many parameters (3 given, 1 needed)"

    def test_multiargadd(self, commandhandler_setup):  # Tests for multi argument commands.
        assert commandhandler_setup.serve("!multiargadd 1 1 1") == 3
        assert commandhandler_setup.serve("!multiargadd 1 2 3") != 5
        assert commandhandler_setup.serve("!multiargadd 1  3") == "Too few parameters (2 given, 3 needed)"
        assert commandhandler_setup.serve("!multiargadd 6 9 2 1 3 4") == "Too many parameters (6 given, 3 needed)"
        assert commandhandler_setup.serve("!multiargadd 6 9") == "Too few parameters (2 given, 3 needed)"
        assert commandhandler_setup.serve("!multiargadd") == "Too few parameters (0 given, 3 needed)"

    def test_sayhi(self, commandhandler_setup):  # Tests for string commands.
        assert commandhandler_setup.serve("!sayhi johnny") == "Hello johnny! :D"
        assert commandhandler_setup.serve("!sayhi johnny madcox") == "Hello johnny madcox! :D"
        assert commandhandler_setup.serve("!sayhi johnny madcox sr") == "Hello johnny madcox sr! :D"
        assert commandhandler_setup.serve("!sayhi ") == "Too few parameters (0 given, 1 needed)"
        assert commandhandler_setup.serve("!sayhi") == "Too few parameters (0 given, 1 needed)"
