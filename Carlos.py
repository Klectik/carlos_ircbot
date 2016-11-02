#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ===================================
# Carlos, IRC Bot
#
# By Klectik. (www.klectik.net)
# ===================================

import ConfigParser
import irclib
import ircbot

# Parse config.ini
config = ConfigParser.ConfigParser()
config.read("config.ini")

nick = config.get("Bot", "nick")
description = config.get("Bot", "description")
password = config.get("Bot", "password")
room = config.get("Connection", "room")
server = config.get("Connection", "server")
port = int(config.get("Connection", "port"))

class Carlos(ircbot.SingleServerIRCBot):
	def __init__(self):
		global nick
		global room
		global server
		global port

		ircbot.SingleServerIRCBot.__init__(self, [(server, port)],nick,description)

	def on_welcome(self,serv,ev):
		serv.join(room)

	def on_privmsg(self,serv,ev):
		author = irclib.nm_to_n(ev.source())
		message = ev.arguments()[0].split(" ")

		if message[-1] == password:

			if not (message[0] in ["!help", "!topic", "!mode", "!say", "!nick", "!me", "!notice"]):
				serv.privmsg(author, "Unknown command. Please type !help to get the command list.")

			if message[0] == "!help" and len(message) == 2:
				serv.privmsg(author, "Command list :")
				serv.privmsg(author, "!help")
				serv.privmsg(author, "!topic")
				serv.privmsg(author, "!mode")
				serv.privmsg(author, "!say")
				serv.privmsg(author, "!nick")
				serv.privmsg(author, "!me")
				serv.privmsg(author, "!notice")
				serv.privmsg(author, "For further information (like syntax or utility) on one of these commands, type :")
				serv.privmsg(author, "!help [!command]")

			if message[0] == "!help" and message[1] == "!help":
				serv.privmsg(author, "[!help]")
				serv.privmsg(author, "    - Syntax : !help [!help | !topic | !mode | !say | !nick | !me | !notice]")
				serv.privmsg(author, "    - Utility : !help command without argument shows the command list. Combined with a command, it shows informations about the command given as an argument.")
				serv.privmsg(author, "      About the detailed syntax : brackets [] contains a choice between multiple elements splitted with |. Braces {} must be replaced. Example : [room | {user}] means that you have the choice between type exactly \"room\" or type a username.")

			if message[0] == "!help" and message[1] == "!topic":
				serv.privmsg(author, "[!topic]")
				serv.privmsg(author, "    - Syntax : !topic {new topic}")
				serv.privmsg(author, "    - Utility : !topic replaces the topic with the new topic given as argument.")

			if message[0] == "!help" and message[1] == "!mode":
				serv.privmsg(author, "[!mode]")
				serv.privmsg(author, "    - Syntax : !mode [room | {user}] [+v | -v | +h | -h | +o | -o | +b [mask] | -b [mask]]")
				serv.privmsg(author, "    - Utility : !mode sets or unsets a mode to an IRC entity.")

			if message[0] == "!help" and message[1] == "!say":
				serv.privmsg(author, "[!say]")
				serv.privmsg(author, "    - Syntax : !say [room | {user}] {message}")
				serv.privmsg(author, "    - Utility : !say sends a message to an IRC entity.")

			if message[0] == "!help" and message[1] == "!nick":
				serv.privmsg(author, "[!nick]")
				serv.privmsg(author, "    - Syntax : !nick {nickname}")
				serv.privmsg(author, "    - Utility : !nick changes bot's nickname.")

			if message[0] == "!help" and message[1] == "!me":
				serv.privmsg(author, "[!me]")
				serv.privmsg(author, "    - Syntax : !me [room | {user}] {action}")
				serv.privmsg(author, "    - Utility : !me sends an action, and yes, that's perfectly useless.")

			if message[0] == "!help" and message[1] == "!notice":
				serv.privmsg(author, "[!notice]")
				serv.privmsg(author, "    - Syntax : !notice [room | {user}] {notice}")
				serv.privmsg(author, "    - Utility : !notice sends a notice to an IRC entity.")

			if message[0] == "!topic":
				if len(message[1:-1]) > 0:
					newtopic = ""
					for elem in message[1:-1]:
						newtopic+=elem+" "
					serv.topic(room, newtopic)
					serv.privmsg(author, "Topic has been replaced by " + newtopic)
				else:
					serv.privmsg(author, "Missing topic. Please type !help !topic for detailed syntax.")

			if message[0] == "!mode":
				if len(message[1:-1]) > 0:
					serv.mode(room, message[2] + " " + message[1])
					serv.privmsg(author, message[1] + " got the mode " + message[2])
				else:
					serv.privmsg(author, "Syntax error. Please type !help !mode for detailed syntax.")

			if message[0] == "!say":
				if len(message[2:-1]) > 0:
					bottle = ""
					for elem in message[2:-1]:
						bottle+=elem+" "
					if message[1] == "room":
						message[1] = room
					serv.privmsg(message[1], bottle)
					serv.privmsg(author, bottle + "envoyé à " + message[1])
				else:
					serv.privmsg(author, "Syntax error. Please type !help !say detailed syntax.")

			if message[0] == "!nick":
				if len(message) > 2:
					serv.nick(message[1])
					serv.privmsg(author, "New nickname : " + message[1])
				else:
					serv.privmsg(author, "Syntax error. Please type !help !nick detailed syntax.")

			if message[0] == "!me":
				if len(message[2:-1]) > 0:
					bottle = ""
					for elem in message[2:-1]:
						bottle+=elem+" "
					if message[1] == "room":
						message[1] = room
					serv.action(message[1], bottle)
					serv.privmsg(author, "Sent on "+message[1]+" with action: "+bottle)
				else:
					serv.privmsg(author, "Syntax error. Please type !help !me detailed syntax.")

			if message[0] == "!notice":
				if len(message[2:-1]) > 0:
					bottle = ""
					for elem in message[2:-1]:
						bottle+=elem+" "
					if message[1] == "room":
						message[1] = room
					serv.notice(message[1], bottle)
					serv.privmsg(author, bottle + "sent as a notice to " + message[1])
				else:
					serv.privmsg(author, "Syntax error. Please type !help !notice detailed syntax.")

		else:
			serv.privmsg(author, "Wrong password")

	def on_kick(self, serv, ev):
		serv.join(room)
