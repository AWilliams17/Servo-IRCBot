import pytest
from servomodules.ircformatting import change_color, change_style


@pytest.fixture(scope='module')
def command_handler_setup(request):
    from servomodules.commandhandler import CommandHandler
    from commandmodules.langmodules import gizoogle, urbandictionary, dictionary
    command_handler = CommandHandler()

    @command_handler.register_command("!gizoogle", "Gizoogles a sentence.", "multi string")
    def gizoogle_s(sentence_arg):
        return gizoogle.gizoogle(sentence_arg)

    @command_handler.register_command("!ud", "Looks up the urban dictionary definition of a word.", "multi string")
    def urban_define(word):
        return urbandictionary.define_word(word)

    @command_handler.register_command("!define", "looks up the owl dictionary definition of a word.")
    def dict_define(word, def_num):
        return dictionary.dictionary_define(word, def_num)

    return command_handler


@pytest.mark.usefixtures('command_handler_setup')
class TestLanguageCommands(object):

    def test_gizoogle(self):
        assert command_handler_setup.serve("!gizoogle this is a test") == "this be a test"

    def test_urbandictionary(self):
        assert command_handler_setup.serve("!ud test") == "Got definition for %s: A process for testing things" % \
               change_style("test", "bold")
        assert command_handler_setup.serve("!ud ijaderogaejoiy") == change_color("Failed to grab definition.", "red")

    def test_dictionary(self):
        assert command_handler_setup.serve("!define test 0") == "Got definition for %s: Metallurgy" % \
               change_style("test", "bold")
