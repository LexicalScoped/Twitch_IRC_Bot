import cfg
import socket
from Logger import Log

class Msg:
    def __init__(self, prefix, user, command, args, text):
        self.prefix = prefix
        self.user = user
        self.command = command
        self.args = args
        self.text = text

class IRC_Server:
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((cfg.SERVER, cfg.PORT))
        self.send_cmd(f'PASS {cfg.TOKEN}')
        self.send_cmd(f'NICK {cfg.NICKNAME}')
        for chan in cfg.CHANNELS:
            self.Join(chan)

    def send_cmd(self, cmd):
        if 'PASS' not in cmd:
            Log(self.Parse_Msg(cmd))
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

    def Parse_Msg(self, received_data):
        prefix = user = command = args = text = " "
        split_data = received_data
        if received_data.startswith(":"):
            split_data = received_data.split(" ", 2)
            prefix = split_data.pop(0)[1:]
            user = self.Parse_Prefix(prefix)
        else:
            split_data = received_data.split(" ", 1)
        command = split_data.pop(0)
        if not split_data[0].startswith(":"):
            split_data = split_data[0].split(":",1)
            args = split_data[0].strip()
            if len(split_data) > 1 :
                text = split_data[1]
        else:
            text = split_data[0][1:]
        return Msg(prefix, user, command, args, text)
    
    def inbound(self):
        while True:
            inbound_queue = self.connection.recv(4096).decode()
            for inbound in inbound_queue.split('\r\n'):
                if len(inbound) > 0:
                    yield (self.Parse_Msg(inbound))