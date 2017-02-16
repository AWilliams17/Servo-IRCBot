# ToDo: Add more logging
# ToDo: Add .ini for connection settings instead of raw_input
# ToDo: More centralized way for command registration

import logging
from time import gmtime, strftime
from os import getcwd, path, makedirs
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from servomodules.commandhandler import CommandHandler
from commandmodules.ps2modules import grabstats, continentstatus
from commandmodules.langmodules import gizoogle, urbandictionary


commandhandler = CommandHandler()
current_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
servo_path = getcwd().split("/bin")[0]
servo_logs = servo_path + "/logs"
if path.exists(servo_logs)is False:
    makedirs(servo_logs)
logging.basicConfig(filename=servo_logs + "/servo %s.log" % current_date, level=logging.DEBUG)


@commandhandler.registercommand("!playerstats", "grabs a players stats")
def ps2player(player):
    return grabstats.grabplayerstats(player)


@commandhandler.registercommand("!continentstatus", "grabs the continent info of a server")
def ps2continent(server):
    return continentstatus.grabcontinentinfo(server)


@commandhandler.registercommand("!gizoogle", "Gizoogles a sentence.", "multi string")
def gizoogles(sentence_arg):
    return gizoogle.gizoogle(sentence_arg)


@commandhandler.registercommand("!ud", "Looks up the urban dictionary definition of a word.", "multi string")
def urbandefine(word):
    return urbandictionary.defineword(word)


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

    def connectionLost(self, reason):
        logging.critical("Connection was lost: %s" % reason)


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
    Hostname = raw_input("Enter Hostname: ")
    Port = int(raw_input("Enter Port: "))
    Channel = raw_input("Enter Channel: ")
    logging.info("-")
    logging.info("Beginning new log: %s" % current_date)
    logging.info("-")
    logging.info("Connecting TCP")
    reactor.connectTCP(Hostname, Port, ServoFactoryClass(Channel, "Servo"))
    logging.info("Running reactor.")
    reactor.run()
