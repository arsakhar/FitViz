from threading import Lock

from scripts.libAnt.profiles.power_profile import PowerProfile
from scripts.libAnt.profiles.speed_cadence_profile import SpeedAndCadenceProfile
from scripts.libAnt.profiles.speed_profile import SpeedProfile
from scripts.libAnt.profiles.cadence_profile import CadenceProfile
from scripts.libAnt.profiles.heartrate_profile import HeartRateProfile
from scripts.libAnt.profiles.fitness_equipment_profile import FitnessEquipmentProfile
from scripts.libAnt.profiles.profile import *


class Factory:
    profiles = {
        HEART_RATE_PROFILE: HeartRateProfile(),
        SPEED_CADENCE_PROFILE: SpeedAndCadenceProfile(),
        POWER_PROFILE: PowerProfile(),
        FITNESS_EQUIPMENT_PROFILE: FitnessEquipmentProfile(),
        SPEED_PROFILE: SpeedProfile(),
        CADENCE_PROFILE: CadenceProfile()
    }

    def __init__(self, callback=None):
        self._filter = None
        self._lock = Lock()
        self._profileMessages = {}
        self._callback = callback

    def enableFilter(self):
        with self._lock:
            if self._filter is None:
                self._filter = {}

    def disableFilter(self):
        with self._lock:
            if self._filter is not None:
                self._filter = None

    def clearFilter(self):
        with self._lock:
            if self._filter is not None:
                self._filter.clear()

    def addToFilter(self, deviceNumber: int):
        with self._lock:
            if self._filter is not None:
                self._filter[deviceNumber] = True

    def removeFromFilter(self, deviceNumber: int):
        with self._lock:
            if self._filter is not None:
                if deviceNumber in self._filter:
                    del self._filter[deviceNumber]

    def parseMessage(self, msg: BroadcastMessage):
        with self._lock:
            if self._filter is not None:
                if msg.deviceNumber not in self._filter:
                    return

            if msg.deviceType in Factory.profiles:
                num = msg.deviceNumber
                type = msg.deviceType

                previous = self._profileMessages[(num, type)] if (num, type) in self._profileMessages else None
                profileMessage = self.profiles[type].getProfileMessage(msg, previous)

                self._profileMessages[(num, type)] = profileMessage

                if callable(self._callback):
                    self._callback(profileMessage)

    def reset(self):
        with self._lock:
            self._profileMessages = {}
