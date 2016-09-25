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
				serv.privmsg(author, "Impossible de comprendre votre commande. Référez-vous à !help pour obtenir la liste des commandes que vous pouvez utiliser.")

			if message[0] == "!help" and len(message) == 2:
				serv.privmsg(author, "Voici les commandes que vous pouvez utiliser :")
				serv.privmsg(author, "!help")
				serv.privmsg(author, "!topic")
				serv.privmsg(author, "!mode")
				serv.privmsg(author, "!say")
				serv.privmsg(author, "!nick")
				serv.privmsg(author, "!me")
				serv.privmsg(author, "!notice")
				serv.privmsg(author, "Pour avoir des détails (comme la syntaxe et l'utilité) sur une de ces commandes, entrez :")
				serv.privmsg(author, "!help [!commande]")

			if message[0] == "!help" and message[1] == "!help":
				serv.privmsg(author, "[!help]")
				serv.privmsg(author, "    - Syntaxe : !help [!help | !topic | !mode | !say | !nick | !me | !notice]")
				serv.privmsg(author, "    - Utilité : La commande !help utilisée seule permet de voir la liste des commandes. Combinée à l'un des paramètres ci-dessus, elle donne des détails sur l'utilisation de la commande précisée.")
				serv.privmsg(author, "      Note sur la syntaxe des aides détaillées : les crochets [] signifient qu'il faut faire un choix entre les propositions séparées par des |. Les accolades {} signifient qu'il faut remplacer ce qui s'y trouve par autre chose. Exemple : [room | {utilisateur}] veut dire qu'il faut, à la place des crochets, soit mettre exactement \"room\" (sans guillemets), soit le nom d'un utilisateur.")

			if message[0] == "!help" and message[1] == "!topic":
				serv.privmsg(author, "[!topic]")
				serv.privmsg(author, "    - Syntaxe : !topic {nouveau topic}")
				serv.privmsg(author, "    - Utilité : La commande !topic permet de modifier le topic du salon par le nouveau topic précisé en paramètre.")

			if message[0] == "!help" and message[1] == "!mode":
				serv.privmsg(author, "[!mode]")
				serv.privmsg(author, "    - Syntaxe : !mode {utilisateur} [+v | -v | +h | -h | +o | -o | +b [masque] | -b [masque]]")
				serv.privmsg(author, "    - Utilité : La commande !mode permet d'attribuer ou de retirer un mode à un utilisateur.")

			if message[0] == "!help" and message[1] == "!say":
				serv.privmsg(author, "[!say]")
				serv.privmsg(author, "    - Syntaxe : !say [room | {utilisateur}] {message}")
				serv.privmsg(author, "    - Utilité : La commande !say permet d'envoyer un message à l'entité précisée en argument.")

			if message[0] == "!help" and message[1] == "!nick":
				serv.privmsg(author, "[!nick]")
				serv.privmsg(author, "    - Syntaxe : !nick {pseudonyme}")
				serv.privmsg(author, "    - Utilité : La commande !nick permet de changer le pseudonyme du bot.")

			if message[0] == "!help" and message[1] == "!me":
				serv.privmsg(author, "[!me]")
				serv.privmsg(author, "    - Syntaxe : !me [room | {utilisateur}] {action}")
				serv.privmsg(author, "    - Utilité : La commande !me permet de faire l'équivalent d'un /me dans un client classique.")

			if message[0] == "!help" and message[1] == "!notice":
				serv.privmsg(author, "[!notice]")
				serv.privmsg(author, "    - Syntaxe : !notice [room | {utilisateur}] {notice}")
				serv.privmsg(author, "    - Utilité : La commande !notice permet d'envoyer une notice au premier argument.")

			if message[0] == "!topic":
				if len(message[1:-1]) > 0:
					newtopic = ""
					for elem in message[1:-1]:
						newtopic+=elem+" "
					serv.topic(room, newtopic)
					serv.privmsg(author, "Le topic a été changé en " + newtopic)
				else:
					serv.privmsg(author, "Merci de préciser un topic pour que je puisse remplacer l'ancien. Référez-vous à !help !topic pour plus de détails.")

			if message[0] == "!mode":
				if len(message[1:-1]) > 0:
					serv.mode(room, message[2] + " " + message[1])
					serv.privmsg(author, message[1] + " a reçu le mode " + message[2])
				else:
					serv.privmsg(author, "Syntaxe incorrecte. Référez-vous à !help !mode pour plus de détails.")

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
					serv.privmsg(author, "Syntaxe incorrecte. Référez-vous à !help !say pour plus de détails.")

			if message[0] == "!nick":
				if len(message) > 2:
					serv.nick(message[1])
					serv.privmsg(author, "Bot renommé en " + message[1])
				else:
					serv.privmsg(author, "Syntaxe incorrecte. Référez-vous à !help !nick pour plus de détails.")

			if message[0] == "!me":
				if len(message[2:-1]) > 0:
					bottle = ""
					for elem in message[2:-1]:
						bottle+=elem+" "
					if message[1] == "room":
						message[1] = room
					serv.action(message[1], bottle)
					serv.privmsg(author, "L'action a été envoyée sur "+message[1]+" avec comme message: "+bottle)
				else:
					serv.privmsg(author, "Syntaxe incorrecte. Référez-vous à !help !me pour plus de détails.")

			if message[0] == "!notice":
				if len(message[2:-1]) > 0:
					bottle = ""
					for elem in message[2:-1]:
						bottle+=elem+" "
					if message[1] == "room":
						message[1] = room
					serv.notice(message[1], bottle)
					serv.privmsg(author, bottle + "envoyé en notice à " + message[1])
				else:
					serv.privmsg(author, "Syntaxe incorrecte. Référez-vous à !help !notice pour plus de détails.")

		else:
			serv.privmsg(author, "Argh, mauvais mot de passe ! :(")

	def on_kick(self, serv, ev):
		serv.join(room)
