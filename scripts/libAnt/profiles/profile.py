from copy import deepcopy
import time
from scripts.libAnt.message import BroadcastMessage

HEART_RATE_PROFILE = 120
SPEED_CADENCE_PROFILE = 121
SPEED_PROFILE = 123
CADENCE_PROFILE = 122
POWER_PROFILE = 11
FITNESS_EQUIPMENT_PROFILE = 17



class ProfileMessage:
    def __init__(self, msg, previous):
        self.previous = previous
        self.msg = deepcopy(msg)
        self.count = previous.count + 1 if previous is not None else 1
        self.timestamp = time.time()
        self.firstTimestamp = previous.firstTimestamp if previous is not None else self.timestamp

    def __str__(self):
        return str(self.msg)

    @staticmethod
    def decode(cls, msg: BroadcastMessage):
        if msg.deviceType in cls.match:
            cls.match[msg.deviceType]()
