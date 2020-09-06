from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage
from scripts.libAnt.profiles.cadence_profile import Default as DefaultCadenceMessage
from scripts.libAnt.profiles.speed_profile import Default as DefaultSpeedMessage

DEFAULT_DATA = 0x00
CHANNEL_PERIOD = 8086
RF_FREQUENCY = 2457


class SpeedAndCadenceProfile:
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
            dataPageMessage = SpeedAndCadenceProfileMessage(msg, previous)

        return dataPageMessage


class SpeedAndCadenceProfileMessage(ProfileMessage):
    """ Message from Speed & Cadence sensor """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]


class Default(SpeedAndCadenceProfileMessage, DefaultCadenceMessage, DefaultSpeedMessage):
    """ Message from Speed & Cadence sensor """

    maxCadenceEventTime = 65536
    maxSpeedEventTime = 65536
    maxSpeedRevCount = 65536
    maxCadenceRevCount = 65536
    maxstaleSpeedCounter = 7
    maxstaleCadenceCounter = 7
    wheelCircumference = 2097

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    def __str__(self):
        ret = '{} Speed: {:.2f}m/s (avg: {:.2f}m/s)\n'.format(super().__str__(),
                                                              self.instantaneousSpeed, self.averageSpeed)
        ret += '{} Cadence: {:.2f}rpm (avg: {:.2f}rpm)\n'.format(super().__str__(),
                                                                 self.instantaneousCadence, self.averageCadence)
        ret += '{} Total Distance: {:.2f}m\n'.format(super().__str__(), self.distanceTraveled())

        return ret

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]

    @lazyproperty
    def cadenceEventTime(self):
        """ Represents the time of the last valid bike cadence event (1/1024 sec) """
        return (self.msg.content[1] << 8) | self.msg.content[0]

    @lazyproperty
    def cumulativeCadenceRevolutionCount(self):
        """ Represents the total number of pedal revolutions """
        return (self.msg.content[3] << 8) | self.msg.content[2]

    @lazyproperty
    def speedEventTime(self):
        """ Represents the time of the last valid bike speed event (1/1024 sec) """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def cumulativeSpeedRevolutionCount(self):
        """ Represents the total number of wheel revolutions """
        return (self.msg.content[7] << 8) | self.msg.content[6]

    def instantaneousSpeed(self):
        """
        :return: The current speed (m/sec)
        """
        return super().instantaneousSpeed

    def distance(self):
        """
        :return: The distance since the last message (m)
        """
        return super().distance

    def distanceTraveled(self):
        """
        :return: The total distance since the first message (m)
        """
        return super().distanceTraveled

    @lazyproperty
    def instantaneousCadence(self):
        """
        :return: RPM
        """
        return super().instantaneousCadence

    @lazyproperty
    def averageCadence(self):
        """
        Returns the average cadence since the first message
        :return: RPM
        """
        return super().averageCadence

    def averageSpeed(self):
        """
        Returns the average speed since the first message
        :return: m/s
        """
        return super().averageSpeed
