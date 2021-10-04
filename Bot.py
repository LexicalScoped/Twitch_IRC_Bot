from Logger import Log
from IRC_Server import IRC_Server

class Bot:
    def __init__(self):
        self.irc_server = IRC_Server()
        self.Read_Inbound()

    def Shout_Out(self, channel, target):
        if target.startswith("@"):
            target = target[1:]
        self.irc_server.Msg_Chan(channel, f'Shout out to {target} - lets show some love and go check out their content at https://twitch.tv/{target}')

    def Handle_Msg(self, Message):
        if Message.prefix != " ":
            Log(Message)
            strings = Message.text.split(" ")
            if strings[0] == "!so":
                self.Shout_Out(Message.args, strings[1])
        if Message.command == "PING":
            Log(Message)
            self.irc_server.Pong(Message.text)

    def Read_Inbound(self):
        for inbound in self.irc_server.inbound():
            if inbound.command != " ":
                self.Handle_Msg(inbound)
            else:
                Log(inbound)