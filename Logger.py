import time

def Write_Line(filepath, line):
    file = open(filepath, 'a')
    file.write(line)
    file.write('\n')
    file.close()

def Server_Log(line):
    Write_Line('log/Server.log', line)

def Channel_Log(channel, line):
    Write_Line(f'log/{channel}.log', line)

def CLI_Log(line):
    print (f'{line}')

def Log(msg):
    timestamp = time.asctime(time.localtime(time.time()))
    CLI_Log(f'<<< ({timestamp}) Pref: {msg.prefix} - User: {msg.user} - CMD: {msg.command} - CMD_Args: {msg.args} - Text: {msg.text}')
    if msg.args.startswith("#") and msg.command == "PRIVMSG":
        Channel_Log(f'{msg.args}', f'{timestamp}: <{msg.user}> {msg.text}')
    else:
        Server_Log(f'<<< {timestamp}: Pref: {msg.prefix} - CMD: {msg.command} - CMD_Args: {msg.args} - Text: {msg.text}')