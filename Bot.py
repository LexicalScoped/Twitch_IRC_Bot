import random
from Logger import Log
from IRC_Server import IRC_Server, Authority


class Bot:
    def __init__(self):
        self.irc_server = IRC_Server()
        self.Read_Inbound()

    def Shout_Out(self, Message):
        if Message.authority >= Authority['MODERATOR'].value:
            strings = Message.text.split(" ")
            target = strings[1]
            if strings[1].startswith("@"):
                target = strings[1][1:]
            self.irc_server.Msg_Chan(Message.args, f'Shout out to {target} - lets show some love and go check out their content at https://twitch.tv/{target}')

    def Coup(self, Message):
        if Message.user == "veggiezombay":
            self.irc_server.Msg_Chan(Message.args, "Coup meeting, 15 minutes, fresh cookies.")
        else:
            self.irc_server.Msg_Chan(Message.args, "Don't let our overlord, veggiezombay, hear you talk like that")

    def EightBall(self, Message):
        answers = [
            "As I see it, yes.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don’t count on it.",
            "It is certain.",
            "It is decidedly so.",
            "Most likely.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Outlook good.",
            "Reply hazy, try again.",
            "Signs point to yes.",
            "Very doubtful.",
            "Without a doubt.",
            "Yes.",
            "Yes – definitely.",
            "You may rely on it. ",
            "Try asking beard_btw",
            "Ask after Lunch"
        ]
        self.irc_server.Msg_Chan(Message.args, f'8ball: {random.choice(answers)}')
    
    def Validate_Dice(self, dice):
        Count = False
        Die = False
        dice = "".join(dice)
        dice = dice.strip()
        if dice.isnumeric():
            Count = 1
            Die = int(dice)
        elif dice.lower().startswith("d"):
            Count = 1
            if dice[1:].isnumeric():
                Die = int(dice[1:])
        elif "d" in dice.lower():
            dice = dice.lower().split("d")
            if len(dice) > 1:
                if dice[0].isnumeric():
                    Count = int(dice[0])
                if dice[1].isnumeric():
                    Die = int(dice[1])
        if Die == 0:
            Die = False
        if Count == 0:
            Count = False
        return Count, Die
            
    def Roll(self, Message):
        rolledDice = []
        Count = 0
        Die = 0
        split_msg = Message.text.split(" ")
        if len(split_msg) > 1:
            Count, Die = self.Validate_Dice(split_msg[1:])
        if Count and Die:
            Die += 1
            if Count == 1:
                rolledDice = [random.randrange(int(Count), int(Die))]
            elif Count > 1:
                rolledDice = [random.randrange(1, int(Die)) for i in range(int(Count))]
            DiceDice = " ".join(map(str, rolledDice))
            resultstring = f"Rolling {Count}d{Die-1} Rolled: " + " ".join(map(str, rolledDice)) + " Total: " + str(sum(rolledDice))
            if len(resultstring) > 500:
                overage = len(resultstring) - 500
                DiceDice = DiceDice[:-overage]
                resultstring = f"Rolling {Count}d{Die-1} Rolled: " + DiceDice + " Total: " + str(sum(rolledDice))
            self.irc_server.Msg_Chan(Message.args, resultstring)
        else:
            self.irc_server.Msg_Chan(Message.args, "No Dice or invalid Dice in roller, please use NumberDNumber, DNumber or Number format ( examples: 2d6 d6 or 6 )")

    def Discord(self, Message):
        self.irc_server.Msg_Chan(Message.args, "My discord can be found here: https://discord.gg/GR8SSMm")

    def GitHub(self, Message): 
        self.irc_server.Msg_Chan(Message.args, "My github can be found here: https://github.com/lexicalscoped")

    def Handle_Msg(self, Message):
        if Message.prefix != " ":
            Log(Message)
            if Message.text.startswith("!"):
                if Message.text.lower().startswith("!so"):
                    self.Shout_Out(Message)
                if Message.text.lower().startswith("!coup"):
                    self.Coup(Message)
                if Message.text.lower().startswith("!8ball"):
                    self.EightBall(Message)
                if Message.text.lower().startswith("!roll"):
                    self.Roll(Message)
                if Message.text.lower().startswith("!discord"):
                    self.Discord(Message)
                if Message.text.lower().startswith("!github"):
                    self.Discord(Message)
        if Message.command == "PING":
            Log(Message)
            self.irc_server.Pong(Message.text)

    def Read_Inbound(self):
        for inbound in self.irc_server.inbound():
            if inbound.command != " ":
                self.Handle_Msg(inbound)
            else:
                Log(inbound)