# ToDo: More centralized way for command registration

import logging
from time import gmtime, strftime
from os import getcwd, path, makedirs
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from servomodules.commandhandler import CommandHandler
from commandmodules.ps2modules import grabstats, continentstatus
from commandmodules.langmodules import gizoogle, urbandictionary
from configparser import ConfigParser

commandhandler = CommandHandler()
servoconfig = ConfigParser()
servo_path = getcwd().split("/bin")[0]
servo_logs_path = servo_path + "/logs"
servo_config_path = servo_path + "/servo.ini"

if not path.exists(servo_logs_path):
    makedirs(servo_logs_path)

current_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
logging.basicConfig(filename=servo_logs_path + "/servo %s.log" % current_date, level=logging.DEBUG)

if not path.exists(servo_config_path):
    logging.warning("The configuration file does not exist. Now generating a new one...")
    print "The Servo.ini file does not exist. I will now generate a new one."
    with open(servo_config_path, 'w') as servo_ini:
        servoconfig.add_section("ConnectionSettings")
        servoconfig.set("ConnectionSettings", "Hostname", "0")
        servoconfig.set("ConnectionSettings", "Port", "0")
        servoconfig.set("ConnectionSettings", "Channel", "0")
        servoconfig.add_section("Planetside2CommandSettings")
        servoconfig.set("Planetside2CommandSettings", "APIKey", "0")
        try:
            servoconfig.write(servo_ini)
        except Exception as e:
            print "I could not generate a new configuration file. :("
            logging.critical("Failed to generate a new configuration file: %r" % e)
        print "I have successfully generated a configuration file."
        logging.info("Successfully generated a new configuration file.")

servoconfig.read(servo_config_path)

apikey = str(servoconfig['Planetside2CommandSettings']['APIKey'])
logging.info("The Planetside API key is set: %s" % apikey)


@commandhandler.registercommand("!playerstats", "grabs a players stats")
def ps2player(player):
    return grabstats.grabplayerstats(player, apikey)


@commandhandler.registercommand("!continentstatus", "grabs the continent info of a server")
def ps2continent(server):
    return continentstatus.grabcontinentinfo(server, apikey)


@commandhandler.registercommand("!gizoogle", "Gizoogles a sentence.", "multi string")
def gizoogles(sentence_arg):
    return gizoogle.gizoogle(sentence_arg)


@commandhandler.registercommand("!ud", "Looks up the urban dictionary definition of a word.", "multi string")
def urbandefine(word):
    return urbandictionary.defineword(word)


@commandhandler.registercommand("!help", "Returns a list of registered commands/specified command description", "optional")
def helpcmd(cmdstring=""):
    if cmdstring is "":
        return "Usage: !help (command) - Registered commands: %s" % ', '.join(commandhandler.registeredcommands.keys())
    else:
        try:
            return "%s: %s" % (cmdstring, commandhandler.registeredcommands.get(cmdstring)[1])
        except TypeError:
            return "Failed to retrieve definition for command: %s" % cmdstring


class Servo(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        logging.info("Connection established.")
        self.setNick("Servo")
        logging.info("Nickname set.")

    def signedOn(self):
        self.join(Channel)

    def privmsg(self, user, channel, message):
        commandresult = commandhandler.serve(message)
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
    Hostname = str(servoconfig['ConnectionSettings']['Hostname'])
    Port = int(servoconfig['ConnectionSettings']['Port'])
    Channel = str(servoconfig['ConnectionSettings']['Channel'])
    logging.info("-")
    logging.info("Beginning new log: %s" % current_date)
    logging.info("-")
    logging.info("Connecting to Hostname %s, Port %s, Channel %s..." % (Hostname, str(Port), Channel))
    reactor.connectTCP(Hostname, Port, ServoFactoryClass(Channel, "Servo"))
    logging.info("Running reactor.")
    reactor.run()
