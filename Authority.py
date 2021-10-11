from enum import Enum

class Authority(Enum):
    CHATUSER = 0
    SUBSCRIBER = 1
    VIP = 2
    MODERATOR = 3
    HOST = 4
    @staticmethod 

    def Get_Auth(tags):
        if "broadcaster" in tags:
            return Authority['HOST'].value
        elif "moderator" in tags:
            return Authority['MODERATOR'].value
        elif "vip" in tags:
            return Authority['VIP'].value
        elif "subscriber" in tags:
            return Authority['SUBSCRIBER'].value
        return Authority['CHATUSER'].value
