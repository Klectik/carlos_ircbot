# Carlos

## Description
Carlos is an IRC robot written in Python with the *python-irclib* library by Joel Rosdahl.

## Installation
1. Put the whole content of this repository into a dedicated folder
2. Configure the robot in *config.ini*
3. Start it with `python start.py` !

## Using
* The robot is protected by a password defined in the config file. Every command must finish with this password, otherwise it will just do nothing. Safety first.
* The commands must be sent by IRC private messages, one command per message.

### Command list

#### !help
* Syntax: !help [!help | !topic | !mode | !say | !nick | !me | !notice]
* Utility: !help command without argument shows the command list. Combined with a command, it shows informations about the command given as an argument.

* About the detailed syntax : brackets [] contains a choice between multiple elements splitted with |. Braces {} must be replaced. Example : [room | {user}] means that you have the choice between type exactly "room" or type a username.
#### !topic
* Syntax: !topic {new topic}
* Utility: !topic replaces the topic with the new topic given as argument.
#### !mode
* Syntax: !mode [room | {user}] [+v | -v | +h | -h | +o | -o | +b [mask] | -b [mask]]
* Utility: !mode sets or unsets a mode to an IRC entity.
#### !say
* Syntax: !say [room | {user}] {message}
* Utility: !say sends a message to an IRC entity.
#### !nick
* Syntax: !nick {nickname}
* Utility: !nick changes bot's nickname.
#### !me
* Syntax: !me [room | {user}] {action}
* Utility: !me sends an action, and yes, that's perfectly useless.
#### !notice
* Syntax: !notice [room | {user}] {notice}
* Utility: !notice sends a notice to an IRC entity.
