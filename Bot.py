from Logger import Log
from IRC_Server import IRC_Server

class Bot:
    def __init__(self):
        self.irc_server = IRC_Server()
        self.Read_Inbound()

    def Shout_Out(self, channel, target):
        if target.startswith("@"):
            self.irc_server.Msg_Chan(channel, f'Hey, this is a shoutout for {target} - lets show some love and go check out their content at https://twitch.tv/{target[1:]}')
        else:
            self.irc_server.Msg_Chan(channel.args, f'Hey, this is a shoutout for @{target} - lets show some love and go check out their content at https://twitch.tv/{target}')

    def Handle_Msg(self, Message):
        if Message.prefix != " ":
            Log(f'<<< Pref: {Message.prefix} - User: {Message.user} - CMD: {Message.command} - CMD_Args: {Message.args} - Text: {Message.text}')
            strings = Message.text.split(" ")
            if strings[0] == "!so":
                self.Shout_Out(Message.args, strings[1])
        if Message.command == "PING":
            self.irc_server.Pong(Message.args)

    def Read_Inbound(self):
        for inbound in self.irc_server.inbound():
            if inbound.command != " ":
                self.Handle_Msg(inbound)
            else:
                Log(inbound)