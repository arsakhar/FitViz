from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage

DEFAULT_DATA = 0x00
CHANNEL_PERIOD = 8102
RF_FREQUENCY = 2457


class CadenceProfile:
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
            dataPageMessage = CadenceProfileMessage(msg, previous)

        return dataPageMessage


class CadenceProfileMessage(ProfileMessage):
    """ Message from Speed & Cadence sensor """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]


class Default(CadenceProfileMessage):
    """ Message from Speed & Cadence sensor """

    maxCadenceEventTime = 65536
    maxCadenceRevCount = 65536
    maxstaleCadenceCounter = 7
    wheelCircumference = 2097

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

        self.staleCadenceCounter = previous.staleCadenceCounter if previous is not None else 0
        self.totalRevolutions = previous.totalRevolutions + self.cadenceRevCountDiff if previous is not None else 0

        if self.previous is not None:
            if self.cadenceEventTime == self.previous.cadenceEventTime:
                self.staleCadenceCounter += 1
            else:
                self.staleCadenceCounter = 0

    def __str__(self):
        ret = '{} Cadence: {:.2f}rpm (avg: {:.2f}rpm)\n'.format(super().__str__(), self.instantaneousCadence, self.averageCadence)
        ret += '{} Total Distance: {:.2f}m\n'.format(super().__str__(), self.distanceTraveled)
        return ret

    @lazyproperty
    def cadenceEventTime(self):
        """ Represents the time of the last valid bike cadence event (1/1024 sec) """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def cumulativeCadenceRevolutionCount(self):
        """ Represents the total number of pedal revolutions """
        return (self.msg.content[7] << 8) | self.msg.content[6]

    @lazyproperty
    def cadenceEventTimeDiff(self):
        if self.previous is None:
            return 0
        elif self.cadenceEventTime < self.previous.cadenceEventTime:
            # Rollover
            return (self.cadenceEventTime - self.previous.cadenceEventTime) + self.maxCadenceEventTime
        else:
            return self.cadenceEventTime - self.previous.cadenceEventTime

    @lazyproperty
    def cadenceRevCountDiff(self):
        if self.previous is None:
            return 0
        elif self.cumulativeCadenceRevolutionCount < self.previous.cumulativeCadenceRevolutionCount:
            # Rollover
            return (self.cumulativeCadenceRevolutionCount - self.previous.cumulativeCadenceRevolutionCount) \
                   + self.maxCadenceRevCount
        else:
            return self.cumulativeCadenceRevolutionCount - self.previous.cumulativeCadenceRevolutionCount

    @lazyproperty
    def distance(self):
        """
        :return: The distance since the last message (m)
        """
        return self.cadenceRevCountDiff * self.wheelCircumference / 1000

    @lazyproperty
    def distanceTraveled(self):
        """
        :return: The total distance since the first message (m)
        """
        return self.totalRevolutions * self.wheelCircumference / 1000

    @lazyproperty
    def instantaneousCadence(self):
        """
        :return: RPM
        """
        if self.previous is None:
            return 0

        if self.cadenceEventTime == self.previous.cadenceEventTime:
            if self.staleCadenceCounter > self.maxstaleCadenceCounter:
                return 0

            return self.previous.instantaneousCadence

        return self.cadenceRevCountDiff * 1024 * 60 / self.cadenceEventTimeDiff

    @lazyproperty
    def averageCadence(self):
        """
        Returns the average cadence since the first message
        :return: RPM
        """
        if self.firstTimestamp == self.timestamp:
            return self.instantaneousCadence
        return self.totalRevolutions * 60 / (self.timestamp - self.firstTimestamp)
