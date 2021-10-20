import cfg
import socket
from Authority import Authority
from Logger import Log

class Msg:
    def __init__(self, tags, prefix, user, command, args, text, authority):
        self.tags = tags
        self.prefix = prefix
        self.user = user
        self.command = command
        self.args = args
        self.text = text
        self.authority = authority

class IRC_Server:
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((cfg.SERVER, cfg.PORT))
        self.send_cmd(f'PASS {cfg.TOKEN}')
        self.send_cmd(f'NICK {cfg.NICKNAME}')
        self.send_cmd(f'CAP REQ :twitch.tv/tags')
        self.send_cmd(f'CAP REQ :twitch.tv/commands')
        for chan in cfg.CHANNELS:
            self.Join(chan)

    def send_cmd(self, cmd):
        if 'PASS' not in cmd and 'PING' not in cmd and 'PONG' not in cmd:
            Log(self.Parse_Msg(cmd, True))
        self.connection.send((cmd + '\r\n').encode())

    def Join(self, channel):
        self.send_cmd(f'JOIN #{channel}')

    def Msg_Chan(self, channel, text):
        self.send_cmd(f'PRIVMSG {channel} :{text}')

    def Pong(self, PING_source):
        self.send_cmd(f'PONG {PING_source}')

    def Parse_Prefix(self, prefix):
        if "!" in prefix:
            return prefix.split("!")[0]
        else:
            return prefix

    def Parse_Tags(self, tags):
        if len(tags.split(";")) >= 2:
            return tags.split(";")[1]
        else:
            return tags

    def Parse_Msg(self, received_data, localuser=False):
        tags = prefix = user = command = args = text = authority = " "
        split_data = received_data
        if received_data.startswith("@"):
            split_data = received_data.split(" ", 3)
            tags = self.Parse_Tags(split_data.pop(0))
            prefix = split_data.pop(0)[1:]
            user = self.Parse_Prefix(prefix)
        elif received_data.startswith(":"):
            split_data = received_data.split(" ", 2)
            prefix = split_data.pop(0)[1:]
            user = self.Parse_Prefix(prefix)
        else:
            split_data = received_data.split(" ", 1)
            if localuser:
                prefix = user = cfg.NICKNAME
        command = split_data.pop(0)
        if not split_data[0].startswith(":"):
            split_data = split_data[0].split(":",1)
            args = split_data[0].strip()
            if len(split_data) > 1 :
                text = split_data[1]
        else:
            text = split_data[0][1:]
        authority = Authority.Get_Auth(tags)
        return Msg(tags, prefix, user, command, args, text, authority)
    
    def inbound(self):
        while True:
            inbound_queue = self.connection.recv(4096).decode()
            for inbound in inbound_queue.split('\r\n'):
                if len(inbound) > 0:
                    yield (self.Parse_Msg(inbound))