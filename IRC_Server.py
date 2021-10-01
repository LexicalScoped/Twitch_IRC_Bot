import cfg
import socket
from Logger import Log

class Msg:
    def __init__(self, prefix, command, args, text):
        self.prefix = prefix
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
        if 'PASS' not in cmd and 'PONG' not in cmd:
            Log(f'>>> {cmd}')
        self.connection.send((cmd + '\r\n').encode())

    def Join(self, channel):
        self.send_cmd(f'JOIN #{channel}')

    def Msg_Chan(self, channel, text):
        self.send_cmd(f'PRIVMSG {channel} :{text}')

    def Pong(self, PING_source):
        self.send_cmd(f'PONG {PING_source}')

    def Parse_Msg(self, received_data):
        prefix = command = args = text = " "
        if len(received_data) == 0:
            return Msg(prefix, command, args, text)
        split_data = received_data.split(" ")    
        if split_data[0].startswith(":"):
            prefix = split_data[0][1:]
            # TODO: build method to break up Prefix to collect only info we need (NICKNAME or SERVER)
            command = split_data[1]
            merge_data = " ".join(split_data[2:])
            if merge_data.startswith(":"):
                text = merge_data.strip()
            else:
                split_data = merge_data.split(":",1)
                args = split_data[0].strip()
                if len(split_data) > 1 :
                    text = split_data[1].strip()
        elif not split_data[0].startswith(":"):
            command = split_data[0]
            args = split_data[1]
        return Msg(prefix, command, args, text)
    
    def inbound(self):
        while True:
            inbound_queue = self.connection.recv(4096).decode()
            for inbound in inbound_queue.split('\r\n'):
                if len(inbound) > 0:
                    yield (self.Parse_Msg(inbound))