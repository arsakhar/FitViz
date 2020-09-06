from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage
import math

STANDARD_POWER_DATA = 0x10
WHEEL_TORQUE_DATA = 0x11
CHANNEL_PERIOD = 4091
RF_FREQUENCY = 2457


class PowerProfile:
    def __init__(self):
        self.dataPages = {
            STANDARD_POWER_DATA: StandardPower,
            WHEEL_TORQUE_DATA: WheelTorque
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
            dataPageMessage = PowerProfileMessage(msg, previous)

        return dataPageMessage


class PowerProfileMessage(ProfileMessage):
    """ Message from Power Meter """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]


class StandardPower(PowerProfileMessage):

    maxAccumulatedPower = 65536
    maxEventCount = 256

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    def __str__(self):
        ret = '{} Average Power: {:d} W'.format(super().__str__(), self.averagePower)
        ret += ' Pedal Power: {:d} %'.format(self.pedalPower)
        ret += ' Instantaneous Power: {:d} W'.format(self.instantaneousPower)

        return ret

    @lazyproperty
    def eventCount(self):
        """
        The update event count field is incremented each time the information in the message is updated.
        There are no invalid values for update event count.
        The update event count in this message refers to updates of the standard Power-Only main data page (0x10)
        :return: Power Event Count
        """
        return self.msg.content[1]

    @lazyproperty
    def pedalPower(self):
        """
        The pedal power data field provides the user’s power contribution (as a percentage) between the left and
        right pedals, as measured by a pedal power sensor. For example, if the user’s power was evenly distributed
        between the left and right pedals, this value would read 50%. If the power was not evenly distributed, for
        example if the pedal power measured 70%, some sensors may or may not know which pedal has the greater power
        contribution. The most significant bit is used to indicate if the pedal power sensor is capable of
        differentiating between the left and right.
        :return: Pedal Power (%)
        """
        if self.msg.content[2] == 255:
            return -1
        else:
            return self.msg.content[2]

    @lazyproperty
    def instantaneousCadence(self):
        """
        The instantaneous cadence field is used to transmit the pedaling cadence recorded from the power sensor.
        This field is an instantaneous value only; it does not accumulate between messages.
        :return: Instantaneous Cadence (rpm)
        """
        if self.msg.content[3] == 255:
            return -1
        else:
            return self.msg.content[3]

    @lazyproperty
    def accumulatedPower(self):
        """
        Accumulated power is the running sum of the instantaneous power data and is incremented at each update
        of the update event count. The accumulated power field rolls over at 65.535kW.
        :return:
        """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def instantaneousPower(self):
        """ Instantaneous power (W) """
        return (self.msg.content[7] << 8) | self.msg.content[6]

    @lazyproperty
    def accumulatedPowerDiff(self):
        if self.previous is None:
            return None
        elif self.accumulatedPower < self.previous.accumulatedPower:
            # Rollover
            return (self.accumulatedPower - self.previous.accumulatedPower) + self.maxAccumulatedPower
        else:
            return self.accumulatedPower - self.previous.accumulatedPower

    @lazyproperty
    def eventCountDiff(self):
        if self.previous is None:
            return None
        elif self.eventCount < self.previous.eventCount:
            # Rollover
            return (self.eventCount - self.previous.eventCount) + self.maxEventCount
        else:
            return self.eventCount - self.previous.eventCount

    @lazyproperty
    def averagePower(self):
        """
        Under normal conditions with complete RF reception, average power equals instantaneous power.
        In conditions where packets are lost, average power accurately calculates power over the interval
        between the received messages
        :return: Average power (Watts)
        """
        if self.accumulatedPowerDiff is None:
            return self.instantaneousPower
        elif self.eventCountDiff is None:
            return self.instantaneousPower
        elif self.eventCountDiff == 0:
            return self.instantaneousPower
        else:
            return self.accumulatedPowerDiff / self.eventCountDiff


class WheelTorque(PowerProfileMessage):

    wheelCircumference = 2097
    maxAccumulatedTorque = 2048
    maxEventCount = 256
    maxWheelTicks = 256
    maxWheelPeriod = 32

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

        self.totalWheelTicks = previous.totalWheelTicks + self.wheelTicksDiff if previous is not None else 0

    def __str__(self):
        ret = '{} Average Torque: {:d} Nm'.format(super().__str__(), self.averageTorque)
        ret += ' Average Power: {:d} W'.format(self.averagePower)

        return ret

    @lazyproperty
    def eventCount(self):
        """
        The update event count field is incremented each time the information in the message is updated.
        There are no invalid values for update event count.
        The update event count in this message refers to updates of the standard Power-Only main data page (0x10)
        :return: Power Event Count
        """
        return self.msg.content[1]

    @lazyproperty
    def wheelTicks(self):
        """
        The wheel ticks field increments with each wheel revolution and is used to calculate linear distance traveled.
        The wheel ticks field rolls over every 256 wheel revolutions, which is approximately 550 meters assuming a
        2m wheel circumference. There are no invalid values for this field. For event-synchronous systems, the
        wheel ticks and update event count increment at the same rate
        :return: Wheel Tick Count (wheel revolutions)
        """
        return self.msg.content[2]

    @lazyproperty
    def instantaneousCadence(self):
        """
        The instantaneous cadence field is used to transmit the pedaling cadence recorded from the power sensor.
        This field is an instantaneous value only; it does not accumulate between messages.
        :return: Instantaneous Cadence (W)
        """
        if self.msg.content[3] == 255:
            return -1
        return self.msg.content[3]

    @lazyproperty
    def wheelPeriod(self):
        """
        The accumulated wheel period is used to indicate the average rotation period of the wheel during the last
        update interval, in increments of 1/2048s. This frequency is chosen because it is a factor of the common
        32.768kHz crystal and because it provides a practical balance between resolution and available data bandwidth.
        Each Wheel Period tick represents a 488-microsecond interval. In event-synchronous systems, the accumulated
        wheel period time stamp field rolls over in 32 seconds. In fixed time interval update systems, the time to
        rollover depends on wheel speed but is greater than 32 seconds. As a rider increases velocity, the period of
        each revolution decreases and the uncertainty due to the resolution of the wheel period time interval becomes
        a proportionally larger part of the calculated speed. This means that the resolution of speed measurement
        changes with speed. For a practical speed range between 20 and 50km/h, the speed resolution is finer than
        0.2km/h; for speeds as high as 80km/h the resolution is less than 0.5km/h.
        :return: Accumulated Wheel Period (1/2048s)
        """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def accumulatedTorque(self):
        """
        The accumulated torque is the cumulative sum of the average torque measured every update event count.
        The accumulated torque field is 2 bytes. The resolution of power measurement changes with speed, but stays
        below the 1-watt level for the most useful speed range. The amount of time required to reach the rollover
        value of the accumulated torque field (2048Nm) varies with power output.
        :return: Accumulated Torque (1/32Nm)
        """
        return (self.msg.content[7] << 8) | self.msg.content[6]

    @lazyproperty
    def accumulatedTorqueDiff(self):
        if self.previous is None:
            return None
        elif self.accumulatedTorque < self.previous.accumulatedTorque:
            # Rollover
            return (self.accumulatedTorque - self.previous.accumulatedTorque) + self.maxAccumulatedTorque
        else:
            return self.accumulatedTorque - self.previous.accumulatedTorque

    @lazyproperty
    def eventCountDiff(self):
        if self.previous is None:
            return None
        elif self.eventCount < self.previous.eventCount:
            # Rollover
            return (self.eventCount - self.previous.eventCount) + self.maxEventCount
        else:
            return self.eventCount - self.previous.eventCount

    @lazyproperty
    def wheelTicksDiff(self):
        if self.previous is None:
            return None
        elif self.wheelTicks < self.previous.wheelTicks:
            # Rollover
            return (self.wheelTicks - self.previous.wheelTicks) + self.maxWheelTicks
        else:
            return self.wheelTicks - self.previous.wheelTicks

    @lazyproperty
    def wheelPeriodDiff(self):
        if self.previous is None:
            return None
        elif self.wheelPeriod < self.previous.wheelPeriod:
            # Rollover
            return (self.wheelPeriod - self.previous.wheelPeriod) + self.maxWheelPeriod
        else:
            return self.wheelPeriod - self.previous.wheelPeriod

    @lazyproperty
    def instantaneousSpeed(self):
        """
        :return: Speed (m/s)
        """
        if self.eventCountDiff is None:
            return None
        elif self.wheelPeriodDiff is None:
            return None
        elif self.wheelPeriodDiff == 0:
            return 0
        else:
            return (3600/1000) * (self.wheelCircumference * self.eventCountDiff) / (self.wheelPeriodDiff / 2048)

    @lazyproperty
    def distance(self):
        """
        :return: The distance since the last message (m)
        """
        if self.wheelTicksDiff is None:
            return None
        else:
            return self.wheelCircumference * self.wheelTicksDiff

    @lazyproperty
    def distanceTraveled(self):
        """
        :return: The total distance since the first message (m)
        """
        if self.totalWheelTicks is None:
            return None
        else:
            return self.totalWheelTicks * self.wheelCircumference

    @lazyproperty
    def averageTorque(self):
        """
        :return: Average torque (Nm)
        """
        if self.accumulatedTorqueDiff is None:
            return None
        elif self.eventCountDiff is None:
            return None
        elif self.eventCountDiff == 0:
            return 0

        return self.accumulatedTorqueDiff / (32 * self.eventCountDiff)

    @lazyproperty
    def averageAngularVelocity(self):
        """
        :return: Average angular velocity (radians/s)
        """
        if self.eventCountDiff is None:
            return None
        elif self.wheelPeriodDiff is None:
            return None
        elif self.wheelPeriodDiff == 0:
            return 0
        else:
            return 2 * math.pi * self.eventCountDiff / (self.wheelPeriodDiff / 2048)

    @lazyproperty
    def averagePower(self):
        """
        :return: Average watts (W)
        """
        if self.averageTorque is None:
            return None
        elif self.averageAngularVelocity is None:
            return None
        else:
            return self.averageTorque * self.averageAngularVelocity
