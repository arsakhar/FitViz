from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage

DEFAULT_DATA = 0x00
CHANNEL_PERIOD = 8070
RF_FREQUENCY = 57


class HeartRateProfile:
    def __init__(self):
        self.dataPages = { }

        self._dataPageMessages = {}

    def getProfileMessage(self, msg, previous):
        dataPage = msg.content[0]

        if dataPage in self.dataPages:
            previous = self._dataPageMessages[dataPage] if dataPage in self._dataPageMessages else None

            dataPageMessage = self.dataPages[dataPage](msg, previous)

            self._dataPageMessages[dataPage] = dataPageMessage

            return dataPageMessage

        else:
            dataPageMessage = HeartRateProfileMessage(msg, previous)

        return dataPageMessage


class HeartRateProfileMessage(ProfileMessage):
    """ Message from Heart Rate Monitor """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    def __str__(self):
        ret = '{} Heart Beat Event Time: {:d} s'.format(super().__str__(), self.heartBeatEventTime)
        ret += ' Heart Beat Count: {:d}'.format(self.heartBeatCount)
        ret += ' Heart Rate: {:d} bpm'.format(self.heartRate)
        return ret

    @lazyproperty
    def heartBeatEventTime(self):
        """
    Represents the time of the last valid
    heart beat event.
        :return: heart beat event time (s)
        """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def heartBeatCount(self):
        """
        A single byte value which increments
        with each heart beat event.
        :return: heart beat count
        """
        return self.msg.content[6]

    @lazyproperty
    def heartRate(self):
        """ 
        Instantaneous heart rate. This value is
        intended to be displayed by the display
        device without further interpretation.
        If Invalid set to 0x00
        """
        return self.msg.content[7]
