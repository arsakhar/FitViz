from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage
import scripts.libAnt.profiles.common_profile as common_profile
import math

TRAINER_TORQUE_DATA = 0x1A
GENERAL_FE_DATA = 0x10
TRAINER_BIKE_DATA = 0x19
MANUFACTURER_IDENTIFICATION = 0x50
PRODUCT_INFORMATION = 0x51
CHANNEL_PERIOD = 8192
RF_FREQUENCY = 2457


class FitnessEquipmentProfile:
    def __init__(self):
        self.dataPages = {
            TRAINER_TORQUE_DATA: TrainerTorqueData,
            GENERAL_FE_DATA: GeneralFEData,
            TRAINER_BIKE_DATA: TrainerBikeData,
            MANUFACTURER_IDENTIFICATION: ManufacturerIdentification,
            PRODUCT_INFORMATION: ProductInformation,
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
            dataPageMessage = FitnessEquipmentProfileMessage(msg, previous)

        return dataPageMessage


class FitnessEquipmentProfileMessage(ProfileMessage):
    """ Message from Fitness Equipment """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]


class TrainerTorqueData(FitnessEquipmentProfileMessage):
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
        ret += ' Average Power: {:d} W'.format(self.averagePower())

        return ret

    @lazyproperty
    def eventCount(self):
        """
        The update event count is incremented each time the information in the data page is updated. There are no
        invalid values for update event count. The update event count in this message refers only to updates of the
        specific trainer torque main data page (0x1A). It should never be used as the update event count of other data
        pages. Trainers may update information at a fixed time interval (time-synchronous updates) or each time a wheel
        rotation event occurs (event-synchronous update). The Wheel Torque message works for both update methods.
        Rollover: The update event count in time-synchronous update systems rolls over at a fixed time interval equal
        to 256 times the update period.
        :return: Event Counter
        """
        return self.msg.content[1]

    @lazyproperty
    def wheelTicks(self):
        """
        The wheel ticks field increments with each wheel revolution and is used to calculate linear distance traveled.
        The wheel ticks field rolls over every 256 wheel revolutions, which is approximately 550 meters assuming a 2m
        wheel circumference. There are no invalid values for this field. For event-synchronous systems, the wheel ticks
        and update event count increment at the same rate
        :return: Wheel Tick Count Increments (wheel revolutions)
        """
        return self.msg.content[2]

    @lazyproperty
    def wheelPeriod(self):
        """
        The accumulated wheel period is used to indicate the average rotation period of the wheel during the
        last update interval, in increments of 1/2048s. This frequency is chosen because it is a factor of the
        common 32.768kHz crystal and because it provides a practical balance between resolution and available data
        bandwidth. Each Wheel Period tick represents a 488-microsecond interval. In event-synchronous systems,
        the accumulated wheel period time stamp field rolls over in 32 seconds. In fixed time interval update systems,
        the time to rollover depends on wheel speed but is greater than 32 seconds. As a rider increases velocity,
        the period of each revolution decreases and the uncertainty due to the resolution of the wheel period time
        interval becomes a proportionally larger part of the calculated speed. This means that the resolution of speed
        measurement changes with speed. For a practical speed range between 20 and 50km/h, the speed resolution is
        finer than 0.2km/h; for speeds as high as 80km/h the resolution is less than 0.5km/h.
        :return: Accumulated Wheel Period (1/2048s)
        """
        return (self.msg.content[4] << 8) | self.msg.content[3]


    @lazyproperty
    def accumulatedTorque(self):
        """
        The accumulated torque is the cumulative sum of the average torque measured every update event count.
        The accumulated torque field is 2 bytes. The resolution of power measurement changes with speed but stays
        below the 1-watt level for the most useful speed range. The amount of time required to reach the rollover value
        of the accumulated torque field (2048Nm) varies with power output.

        :return: Accumulated Torque (1/32Nm)
        """
        return (self.msg.content[6] << 8) | self.msg.content[5]

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
        else:
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


class GeneralFEData(FitnessEquipmentProfileMessage):
    maxAccumulatedElapsedTime = 64
    maxAccumulatedDistanceTraveled = 256

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

        self.elapsedTime = previous.elapsedTime + self.accumulatedElapsedTimeDiff if previous is not None else 0
        self.distanceTraveled = previous.distanceTraveled + self.accumulatedDistanceTraveledDiff \
            if previous is not None else 0

    def __str__(self):
        ret = '{} Elapsed Time: {:d} s'.format(super().__str__(), self.elapsedTime)
        ret += ' Distance Traveled: {:d} s'.format(self.distanceTraveled)
        ret += ' Speed: {:d} m/s'.format(self.instantaneousSpeed)
        ret += ' Heart Rate: {:d} bpm'.format(self.heartRate)
        return ret

    @lazyproperty
    def accumulatedElapsedTime(self):
        """
        The elapsed time field is a required field for all FE, and is used to track the elapsed time during the
        session to 0.25 second (1 message) resolution. This field is an accumulated value field and will roll over
        every 64 seconds traveled. Refer to section 9.1 for guidance on using accumulated values. Note that the elapsed
        time field shall [self-verify] only increment when the fitness equipment is in the IN_USE state.
        :return: Accumulated Elapsed Time Since Start of Workout (.25 seconds)
        """
        return self.msg.content[2] * .25

    @lazyproperty
    def accumulatedDistance(self):
        """
        The distance field is only required on rowers, Nordic skiers, treadmills, and trainers, and is used to track
        the total distance covered during the session to 1 meter of resolution. This field is an accumulated value
        field and will roll over with every 256 meters traveled. Refer to section 9.1 for guidance on using accumulated
        values. There is no invalid value for this field. The Capabilities Bit Field in Byte 7 is used to indicate
        whether data in this field should be interpreted (refer to Table 8-9).
        :return: Accumulated Distance Traveled Since Start of Workout (metres)
        """
        return self.msg.content[3]

    @lazyproperty
    def instantaneousSpeed(self):
        """
        The speed field is only required on rowers, Nordic skiers, treadmills, and trainers, and is a 2 byte value
        representing the instantaneous speed sent in units of 0.001 m/s. If the speed field is not used, it should
        be set to invalid. Note that this field may be used to indicate real or virtual speed as indicated by the
        virtual speed flag (section 8.5.2.6.2).
        :return: Instantaneous Speed (0.001 m/s)
        """
        _instantaneousSpeed = ((self.msg.content[5] << 8) | self.msg.content[4])

        if _instantaneousSpeed == 65535:
            return -1
        else:
            return  _instantaneousSpeed * .001

    @lazyproperty
    def heartRate(self):
        """
        The heart rate data may be obtained from hand contact sensors on the FE, from an EM (5kHz) wireless heart rate
        monitor worn by the user, from an ANT+ heart rate monitor, or from another type of device. The source of the
        heart rate information shall [self-verify] be indicated using the capabilities bit field (refer to Table 8-9).
        In most cases, the user will be wearing an ANT+ HRM paired to his/her ANT+ display. In this case the
        display/controller may either:
        • Ignore the heart rate data coming from the fitness equipment, and use the data received directly from the ANT+
        heart rate monitor.
        • Use the heart rate data obtained from the ANT+ heart rate monitor and retransmitted by the fitness equipment.
        The display can then close its ANT+ heart rate channel to reduce its power consumption. It is recommended that
        the display also uses the heart rate data received in byte 6 if an ANT+ HRM is not available and the fitness
        equipment obtains heart rate from another source.
        Note that if heart rate is determined from hand contact sensors on the FE, data will only be available
        intermittently.
        :return: Instantaneous Heart Rate (bpm)
        """
        if self.msg.content[6] == 255:
            return -1
        else:
            return self.msg.content[6]

    @lazyproperty
    def accumulatedElapsedTimeDiff(self):
        if self.previous is None:
            return None
        elif self.accumulatedElapsedTime < self.previous.accumulatedElapsedTime:
            # Rollover
            return (self.accumulatedElapsedTime - self.previous.accumulatedElapsedTime) + self.maxAccumulatedElapsedTime
        else:
            return self.accumulatedElapsedTime - self.previous.accumulatedElapsedTime

    @lazyproperty
    def accumulatedDistanceTraveledDiff(self):
        if self.previous is None:
            return None
        elif self.accumulatedDistance < self.previous.accumulatedDistance:
            # Rollover
            return (self.accumulatedDistance - self.previous.accumulatedDistance) + self.maxAccumulatedDistanceTraveled
        else:
            return self.accumulatedDistance - self.previous.accumulatedDistance


class TrainerBikeData(FitnessEquipmentProfileMessage):
    maxAccumulatedPower = 65536
    maxEventCount = 256

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    def __str__(self):
        ret = '{} Average Power: {:d} W'.format(super().__str__(), self.averagePower)
        ret += ' Instantaneous Power: {:d} W'.format(self.instantaneousPower)

        return ret

    @lazyproperty
    def eventCount(self):
        """
        The update event count field is incremented each time the information in data page 25 is updated. There are
        no invalid values for update event count. The time between updates must be a regular time -based interval
        for accurate averaging.

        :return: Event Counter
        """
        return self.msg.content[1]

    @lazyproperty
    def instantaneousCadence(self):
        """
        The instantaneous cadence field is used to report the pedaling cadence recorded by the trainer. This is an
        instantaneous value only and does not accumulate between messages. The value 0xFF is sent in this field to
        indicate that the trainer cannot measure pedaling cadence. 0xFF is interpreted as an invalid value and is
        ignored by the display.
        :return: Crank Cadence (RPM)
        """
        if self.msg.content[2] == 255:
            return -1
        else:
            return self.msg.content[2]

    @lazyproperty
    def accumulatedPower(self):
        """
        Accumulated power is the running sum of the instantaneous power data and is incremented at each update of the
        update event count. The accumulated power field rolls over at 65536W. At 2Hz power event updates, there are
        sufficient buffers over all power levels.
        :return: Accumulated Power (watts)
        """
        _accumulatedPower = (self.msg.content[4] << 8) | self.msg.content[3]

        if _accumulatedPower == 65535:
            return -1
        else:
            return _accumulatedPower

    @lazyproperty
    def instantaneousPower(self):
        """
        Instantaneous power calculated by the FE is sent as an unsigned 12-bit value. This field may be used to display
        power; however, it should not be used for calculations (e.g. of average power).
        :return: Instantaneous Power (watts)
        """
        _instantaneousPower = ((self.msg.content[6] & 15) << 8) | self.msg.content[5]

        if _instantaneousPower == 65535:
            return -1
        else:
            return _instantaneousPower

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


class ManufacturerIdentification(FitnessEquipmentProfileMessage):
    def __new__(cls, msg, previous):
        return common_profile.ManufacturerInformation(msg, previous)


class ProductInformation(FitnessEquipmentProfileMessage):
    def __new__(cls, msg, previous):
        return common_profile.ProductInformation(msg, previous)
