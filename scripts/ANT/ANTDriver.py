from scripts.libAnt.drivers.usb import USBDriver
from scripts.libAnt.node import Node
from scripts.libAnt.constants import *
from scripts.libAnt.profiles.factory import Factory
from time import sleep
from enum import Enum
import scripts.libAnt.profiles.power_profile as power_profile
import scripts.libAnt.profiles.speed_cadence_profile as speed_cadence_profile
import scripts.libAnt.profiles.speed_profile as speed_profile
import scripts.libAnt.profiles.cadence_profile as cadence_profile
import scripts.libAnt.profiles.heartrate_profile as heartrate_profile
import scripts.libAnt.profiles.fitness_equipment_profile as fitness_equipment_profile
from scripts.libAnt.profiles.profile import *


class ANTMode(Enum):
    SCAN = 1
    LISTEN = 2


class ANTDriver:
    profiles = {
        HEART_RATE_PROFILE: heartrate_profile,
        SPEED_CADENCE_PROFILE: speed_cadence_profile,
        POWER_PROFILE: power_profile,
        FITNESS_EQUIPMENT_PROFILE: fitness_equipment_profile,
        SPEED_PROFILE: speed_profile,
        CADENCE_PROFILE: cadence_profile
    }

    def __init__(self):
        self.vendorID = 0x0fcf  # vendor ID for Wahoo Kickr ANT+ Dongle
        self.productID = 0x1009  # product ID for Wahoo Kickr ANT+ Dongle

        self.node = None
        self.messageHandler = None

        self.mode = ANTMode.LISTEN

        self.activeChannels = []
        self.broadcastingDevices = []
        self.broadcastingProfiles = []
        self.profileMessage = None
        self.messageCallback = None

    # pmsg is a profile message (parent is broadcast message) containing message content.
    # message content contains payload and extended content
    # An example payload is 10 76 FF 00 01 2F 00 00 (8-bytes). All payloads are always 8-bytes.
    def onSuccess(self, pmsg):
        deviceNumber = pmsg.msg.deviceNumber
        deviceType = pmsg.msg.deviceType

        if self.mode == ANTMode.SCAN:
            if deviceNumber not in self.broadcastingDevices:
                self.broadcastingDevices.append(deviceNumber)
            if deviceType not in self.broadcastingProfiles:
                self.broadcastingProfiles.append(deviceType)

        elif self.mode == ANTMode.LISTEN:
            self.profileMessage = pmsg

            if self.messageCallback is not None:
                self.messageCallback(self.profileMessage)

    def onFailure(self, e):
        print(e)

    def listen(self, listenCallback = None):
        self.mode = ANTMode.LISTEN

        if listenCallback is not None:
            self.messageCallback = listenCallback

    def scan(self, scanCallBack = None, timeout=5):
        self.mode = ANTMode.SCAN

        self.disconnect()
        self.configureRxScanMode()
        self.connect()

        sleep(timeout)  # scan for devices for 10 seconds

        if not self.broadcastingDevices:
            self.disconnect()

        if scanCallBack is not None:
            scanCallBack(self.broadcastingDevices)

    def configureRxScanMode(self):
        if self.node is None:
            # The USB ANT+ dongle.
            antDongleDriver = USBDriver(vid=self.vendorID, pid=self.productID)

            # create an ANT+ node for communication
            self.node = Node(antDongleDriver)

        # configure ANT+ node
        self.node.enableRxScanMode(networkKey=ANTPLUS_NETWORK_KEY,
                                   channelType=CHANNEL_TYPE_ONEWAY_RECEIVE,
                                   channelId=True,
                                   frequency=2457,
                                   rssi=True,
                                   rxTimestamp=True)

        self.messageHandler = Factory(self.onSuccess)

    def getAvailableChannel(self):
        for channel in range(0, 8):
            if channel not in self.activeChannels:
                self.activeChannels.append(channel)

                return channel

        return None

    def configureChannels(self):
        if self.node is None:
            # The USB ANT+ dongle.
            antDongleDriver = USBDriver(vid=self.vendorID, pid=self.productID)

            # create an ANT+ node for communication
            self.node = Node(antDongleDriver)

        if len(self.broadcastingProfiles) > 8:
            return

        for profile in self.broadcastingProfiles:
            if profile in self.profiles:
                channelPeriod = self.profiles[profile].CHANNEL_PERIOD
                rfFrequency = self.profiles[profile].RF_FREQUENCY

            else:
                channelPeriod = 8192
                rfFrequency = 57

            channel = self.getAvailableChannel()

            if channel is None:
                break

            # configure ANT+ node
            self.node.enableChannel(channel=channel,
                                    deviceType=profile,
                                    frequency=rfFrequency,
                                    channelPeriod=channelPeriod)

        self.messageHandler = Factory(self.onSuccess)

    def connect(self):
        # Starts a thread that reads from driver
        self.node.start(onSuccess=self.messageHandler.parseMessage, onFailure=self.onFailure)

    def disconnect(self):
        if self.node is not None:
            if self.node.isRunning():
                self.node.stop()

    def reset(self):
        if self.messageHandler is not None:
            self.messageHandler._profileMessages = {}
