import socket
import random
import sys

from time import sleep
from insults import insults
from math import *
from mathParser import evaluate

operators = ["LambdaPI"]
server = "irc.openredstone.org"
channel = "#openredstone"
#channel = "#botspam"
botnick = "LambBot"

def parseText(text):
    if text != "":
        if text[0] == ":":
            words = text.split(" ")   #split text into words
            sender = words[0][1:text.find("!")]   #get sender
            command = words[1]  #get command              
            if (sender == "OREBuild" or sender == "ORESchool" or sender == "ORESurvival") and (command == "PRIVMSG"): 
                content = words[4:]    #check if going to minecraft
                player = words[3][4:-2]
            else:
                content = words[3:]
                if len(content) != 0:
                    content[0] = content[0][1:]  #strip leading ":"
                player = "-1"
            tokens = []
            if len(content) != 0:
                tokens = content[0].split("$", 1)
            if len(tokens) == 2 and (tokens[0] == "" or tokens[0] == "\x0f"):
                botcommand, content = tokens[1], content[1:]
                botcommand = botcommand.strip()
            else:
                botcommand = None
            return sender, command, player, botcommand, content
    return "-1", "-1", "-1", None, []


def sendMsg(msg, sender, player):
    if sender == '-1':
        return
    if player == '-1':
        irc.send('PRIVMSG ' + sender + ' :' + msg + '\r\n')
        return
    if player != '-1':
        irc.send('PRIVMSG ' + sender + ' :/msg ' + player + ' ' + msg + '\r\n')
        return


def ping(): 
  irc.send("PONG :pingis\n")


def insult(sender, player, content):
    if content == []:
        sendMsg(insults[random.randint(0, len(insults)-1)], sender, player)
    else:
        sendMsg("Usage: $insult", sender, player)
def wiki(sender, player, content):
    if len(content) == 1:
        sendMsg("https://en.wikipedia.org/wiki/" + content[0], sender, player)
    else:
        sendMsg("Usage: $wiki [article]", sender, player)
def help(sender, player, content):
    if content == []:
        sendMsg("Commands: %s" % ", ".join(commands.keys()), sender, player)
    else:
        sendMsg("Usage: $help", sender, player)
def chikn(sender, player, content):
    if content == []:
        sendMsg("Bwak", sender, player)
    else:
        sendMsg("Usage: $chikn", sender, player)
def calc(sender, player, content):
    if content != []:
        expression = ' '.join(content).strip()
        #print expression
        try:
            result = evaluate(expression)
            sendMsg(str(result), sender, player)
        except Exception, info:
            sendMsg("Exception: %s" %(info), sender, player)
    else:
        sendMsg("Usage: $calc [expression]", sender, player)

def bitly(sender, player, content):
    if content != []:
        pass

def scramble(sender, player, content):
    if content != []:
        pass


def receive(connection):
    text = connection.recv(4096)
    print text
    sender, command, player, botcommand, content = parseText(text)
    if text.find("PING") == 0: 
        print "PONG"
        ping()
    if command == "PRIVMSG" and botcommand != None and botcommand != "":
        handler = commands.get(botcommand)
        if handler == None:
            placeholder = None
            #sendMsg("Command not found: do >help for list of commands.", sender, player)
        else:
            handler(sender, player, content)

commands = {
    "insult": insult,
    "wiki": wiki,
    "help": help,
    "chikn": chikn,
    "calc": calc
}

password = sys.argv[1]
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print "connecting to: " + server
irc.connect((server, 6667)) #connects to the server
irc.send("PASS " + password + "\r\n")
irc.send("USER "+ botnick + " " + botnick + " " + botnick + " :LambdaBot\n") #user authentication
irc.send("NICK "+ botnick +"\n")                            #sets nick
sleep(5)
irc.send("JOIN " + channel + " \r\n")        #join the chan

irc.send('PRIVMSG ' + channel + ' :Hello! This Is LambBot. Do $help for commands.\r\n')
#irc.send('PRIVMSG ' + channel + ' :JXU\'s bot is superior\r\n')
sleep(2)


while True:
    receive(irc)
    sleep(1)

