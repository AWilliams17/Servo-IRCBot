import pytest
from servomodules.ircformatting import changecolor, changestyle

@pytest.fixture(scope='module')
def commandhandler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from commandmodules.langmodules import gizoogle, urbandictionary
    commandhandler = CommandHandler()

    @commandhandler.registercommand("!gizoogle", "Gizoogles a sentence.", "multi string")
    def gizoogles(sentence_arg):
        return gizoogle.gizoogle(sentence_arg)

    @commandhandler.registercommand("!ud", "Looks up the urban dictionary definition of a word.", "multi string")
    def urbandefine(word):
        return urbandictionary.defineword(word)

    return commandhandler


@pytest.mark.usefixtures('commandhandler_setup')
class Test_LanguageCmds(object):

    def test_gizoogle(self, commandhandler_setup):
        assert commandhandler_setup.serve("!gizoogle this is a test") == "this be a test"

    def test_urbandictionary(self, commandhandler_setup):
        assert commandhandler_setup.serve("!ud test") == "Got definition for %s: A process for testing things" % \
                                                         changestyle("test", "bold")
        assert commandhandler_setup.serve("!ud ijaderogaejoiy") == changecolor("Failed to grab definition.", "red")