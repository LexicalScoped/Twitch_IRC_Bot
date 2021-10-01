# LexicalChatBot

A Twitch IRC Chat bot made using python and sockets instead of twitchio.
The purpose of this project was to deepen my understanding of coding with python, leveraging lower level/base modules.

## Used for Moderating Twitch Chat.

This is a bot underdevelopment to provide chat modding capabilities, as well as commands for chat interaction/feedback.

## Version History

* 0.1
    * Initial [commit](https://github.com/LexicalScoped/Twitch_IRC_Bot/commit/8a12205c9c8879d7ac65bbef2f1636ae5c08b562)

## Getting Started

### Dependencies

Built on:
* Ubuntu 18.04
* Python 3.8.0

### Installing

* Load files into directory
* Create cfg.py with the following
```
TOKEN = "oauth:<secret key from twitch>"
SERVER = "irc.chat.twitch.tv"
PORT = 6667
NICKNAME = "<username from account of oauth token"
CHANNELS = { "channel", "or channels", "you want the bot to join" }
SERVER_ALIAS = "tmi.twitch.tv"
```


### Executing program

Execute from the commandline.
```
python3 TCB.py
```

## Authors

Lexical Scoped

[Twitch](https://twitch.tv/LexicalScoped)
[GitHub](https://github.com/LexicalScoped)
[Twitter](https://twitter.com/LScoped)
[YouTube](https://www.youtube.com/channel/UCeH2wW-3hU6OF4jxvH9VCjQ)


