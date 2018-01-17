# ToDo: More centralized way for command registration

import logging
from time import gmtime, strftime
from os import getcwd, path, makedirs
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from servomodules.commandhandler import CommandHandler
from commandmodules.ps2modules import grabstats, continentstatus
from commandmodules.langmodules import gizoogle, urbandictionary, dictionary
from configparser import ConfigParser

CommandHandler = CommandHandler()
servo_config = ConfigParser()
servo_path = getcwd().split("/bin")[0]
servo_logs_path = servo_path + "/logs"
servo_config_path = servo_path + "/servo.ini"

if not path.exists(servo_logs_path):
    makedirs(servo_logs_path)

current_date = strftime("%Y-%m-%d - %H-%M-%S", gmtime())
logging.basicConfig(filename="%s\servo %s.log" % (servo_logs_path, current_date), level=logging.DEBUG)

if not path.exists(servo_config_path):
    logging.warning("The configuration file does not exist. Now generating a new one...")
    print "The Servo.ini file does not exist. I will now generate a new one."
    with open(servo_config_path, 'w') as servo_ini:
        servo_config.add_section("ConnectionSettings")
        servo_config.set("ConnectionSettings", "Hostname", "0")
        servo_config.set("ConnectionSettings", "Port", "0")
        servo_config.set("ConnectionSettings", "Channel", "0")
        servo_config.set("ConnectionSettings", "Nickname", "Servo")
        servo_config.add_section("Planetside2CommandSettings")
        servo_config.set("Planetside2CommandSettings", "APIKey", "0")
        try:
            servo_config.write(servo_ini)
        except Exception as e:
            print "I could not generate a new configuration file. :("
            logging.critical("Failed to generate a new configuration file: %r" % e)
        print "I have successfully generated a configuration file."
        logging.info("Successfully generated a new configuration file.")

servo_config.read(servo_config_path)

api_key = str(servo_config['Planetside2CommandSettings']['APIKey'])
nick_name = str(servo_config['ConnectionSettings']['Nickname'])
logging.info("The Planetside API key is set: %s" % api_key)


@CommandHandler.registercommand("!playerstats", "grabs a players stats")
def ps2_player(player):
    return grabstats.grabplayerstats(player, api_key)


@CommandHandler.registercommand("!continentstatus", "grabs the continent info of a server")
def ps2_continent(server):
    return continentstatus.grabcontinentinfo(server, api_key)


@CommandHandler.registercommand("!gizoogle", "gizoogles a sentence.", "multi string")
def gizoogle_s(sentence_arg):
    return gizoogle.gizoogle(sentence_arg)


@CommandHandler.registercommand("!ud", "looks up the urban dictionary definition of a word.", "multi string")
def urban_define(word):
    return urbandictionary.defineword(word)


@CommandHandler.registercommand("!define", "looks up the owl dictionary definition of a word.")
def dict_define(word, defnum):
    return dictionary.dictionarydefine(word, defnum)


@CommandHandler.registercommand("!help", "returns a list of registered commands/specified command description", "optional")
def help_cmd(commandstring=""):
    if commandstring is "":
        return "Usage: !help (command) - Registered commands: %s" % ', '.join(CommandHandler.registeredcommands.keys())
    else:
        try:
            return "%s: %s" % (commandstring, CommandHandler.registeredcommands.get(commandstring)[1])
        except TypeError:
            return "Failed to retrieve definition for command: %s" % commandstring


class Servo(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        logging.info("Connection established.")
        self.setNick(nick_name)
        logging.info("Nickname set.")

    def signedOn(self):
        self.join(CHANNEL)

    def privmsg(self, user, channel, message):
        commandresult = CommandHandler.serve(message)
        if commandresult is not None:
            logging.info("Got command call: %s" % message)
            self.msg(channel, commandresult)


class ServoFactoryClass(protocol.ClientFactory):
    protocol = Servo

    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        logging.error("Connection was lost: %s" % reason)
        logging.info("attempting to reconnect...")
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        logging.critical("Connection failed: %s" % reason)


if __name__ == '__main__':
    HOSTNAME = str(servo_config['ConnectionSettings']['Hostname'])
    PORT = int(servo_config['ConnectionSettings']['Port'])
    CHANNEL = str(servo_config['ConnectionSettings']['Channel'])
    logging.info("-")
    logging.info("Beginning new log: %s" % current_date)
    logging.info("-")
    logging.info("Connecting to Hostname %s, Port %s, Channel %s..." % (HOSTNAME, str(PORT), CHANNEL))
    reactor.connectTCP(HOSTNAME, PORT, ServoFactoryClass(CHANNEL, nick_name))
    logging.info("Running reactor.")
    reactor.run()
