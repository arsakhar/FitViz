from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage

DEFAULT_DATA = 0x00
CHANNEL_PERIOD = 8118
RF_FREQUENCY = 2457


class SpeedProfile:
    def __init__(self):
        self.dataPages = {
            DEFAULT_DATA: Default
        }

        self._dataPageMessages = {}

    def getProfileMessage(self, msg, previous):
        dataPage = msg.content[0]

        if dataPage in self.dataPages:
            previous = self._dataPageMessages[dataPage] if dataPage in self._dataPageMessages else None

            dataPageMessage = self.dataPages[dataPage](msg, previous)

            self._dataPageMessages[dataPage] = dataPageMessage

            return dataPageMessage

        else:
            dataPageMessage = SpeedProfileMessage(msg, previous)

        return dataPageMessage


class SpeedProfileMessage(ProfileMessage):
    """ Message from Speed & Cadence sensor """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]


class Default(SpeedProfileMessage):
    """ Message from Speed & Cadence sensor """

    maxSpeedEventTime = 65536
    maxSpeedRevCount = 65536
    maxStaleSpeedCounter = 7
    wheelCircumference = 2097

    def __init__(self, msg, previous):
        super().__init__(msg, previous)
        self.staleSpeedCounter = previous.staleSpeedCounter if previous is not None else 0
        self.totalSpeedRevolutions = previous.totalSpeedRevolutions + self.speedRevCountDiff \
            if previous is not None else 0

        if self.previous is not None:
            if self.speedEventTime == self.previous.speedEventTime:
                self.staleSpeedCounter += 1
            else:
                self.staleSpeedCounter = 0

    def __str__(self):
        ret = '{} Speed: {:.2f}m/s (avg: {:.2f}m/s)\n'.format(super().__str__(), self.instantaneousSpeed,
                                                              self.averageSpeed)
        ret += '{} Total Distance: {:.2f}m\n'.format(super().__str__(), self.distanceTraveled)
        return ret

    @lazyproperty
    def speedEventTime(self):
        """ Represents the time of the last valid bike speed event (1/1024 sec) """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def cumulativeSpeedRevolutionCount(self):
        """ Represents the total number of wheel revolutions """
        return (self.msg.content[7] << 8) | self.msg.content[6]

    @lazyproperty
    def speedEventTimeDiff(self):
        if self.previous is None:
            return 0
        elif self.speedEventTime < self.previous.speedEventTime:
            # Rollover
            return (self.speedEventTime - self.previous.speedEventTime) + self.maxSpeedEventTime
        else:
            return self.speedEventTime - self.previous.speedEventTime

    @lazyproperty
    def speedRevCountDiff(self):
        if self.previous is None:
            return 0
        elif self.cumulativeSpeedRevolutionCount < self.previous.cumulativeSpeedRevolutionCount:
            # Rollover
            return (self.cumulativeSpeedRevolutionCount - self.previous.cumulativeSpeedRevolutionCount) \
                   + self.maxSpeedRevCount
        else:
            return self.cumulativeSpeedRevolutionCount - self.previous.cumulativeSpeedRevolutionCount

    @lazyproperty
    def instantaneousSpeed(self):
        """
        :return: The current speed (m/sec)
        """
        if self.previous is None:
            return 0
        if self.speedEventTime == self.previous.speedEventTime:
            if self.staleSpeedCounter > self.maxStaleSpeedCounter:
                return 0

            return self.previous.instantaneousSpeed

        return self.speedRevCountDiff * 1.024 * self.wheelCircumference / self.speedEventTimeDiff

    @lazyproperty
    def distance(self):
        """
        :return: The distance since the last message (m)
        """
        return self.speedRevCountDiff * self.wheelCircumference / 1000

    @lazyproperty
    def distanceTraveled(self):
        """
        :return: The total distance since the first message (m)
        """
        return self.totalSpeedRevolutions * self.wheelCircumference / 1000

    @lazyproperty
    def averageSpeed(self):
        """
        Returns the average speed since the first message
        :return: m/s
        """
        if self.firstTimestamp == self.timestamp:
            return self.instantaneousSpeed
        return self.distanceTraveled / (self.timestamp - self.firstTimestamp)
