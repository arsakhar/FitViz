import threading
from queue import Queue, Empty
from time import sleep

from scripts.libAnt.drivers.driver import Driver
from scripts.libAnt.message import *


class Network:
    def __init__(self, key: bytes = b'\x00' * 8, name: str = None):
        self.key = key
        self.name = name
        self.number = 0

    def __str__(self):
        return self.name


# Thread for writing and reading messages TO/FROM ANT+ driver
class Pump(threading.Thread):
    def __init__(self, driver: Driver, initMessages, out: Queue, onSucces, onFailure):
        super().__init__()
        self._stopper = threading.Event()
        self._driver = driver
        self._out = out
        self._initMessages = initMessages
        self._waiters = []
        self._onSuccess = onSucces
        self._onFailure = onFailure

    def stop(self):
        self._driver.abort()
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def run(self):
        while not self.stopped():
            try:
                with self._driver as d:
                    # Startup
                    rst = SystemResetMessage()
                    self._waiters.append(rst)
                    d.write(rst)
                    for m in self._initMessages:
                        self._waiters.append(m)
                        d.write(m)

                    while not self.stopped():
                        #  Write
                        try:
                            outMsg = self._out.get(block=False)
                            self._waiters.append(outMsg)
                            d.write(outMsg)
                        except Empty:
                            pass

                        # Read
                        try:
                            msg = d.read(timeout=1)

                            if msg.type == MESSAGE_CHANNEL_EVENT:
                                # This is a response to our outgoing message
                                for w in self._waiters:
                                    if w.type == msg.content[1]:  # ACK
                                        self._waiters.remove(w)
                                        #  TODO: Call waiter callback from tuple (waiter, callback)
                                        break
                            # if message ID (type) is a broadcast message (received message)
                            elif msg.type == MESSAGE_CHANNEL_BROADCAST_DATA:
                                bmsg = BroadcastMessage(msg.type, msg.content).build(msg.content)
                                self._onSuccess(bmsg)
                        except Empty:
                            pass
            except Exception as e:
                self._onFailure(e)
            except:
                pass
            self._waiters.clear()
            sleep(1)


class Node:
    def __init__(self, driver: Driver, name: str = None):
        self._driver = driver
        self._name = name
        self._out = Queue()
        self._init = []
        self._pump = None
        self._configMessages = Queue()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self, onSuccess, onFailure):
        if not self.isRunning():
            self._pump = Pump(self._driver, self._init, self._out, onSuccess, onFailure)
            self._pump.start()

    """
    Section - 9.5.4.5 - Control Message - Open Rx Scan Mode (0x5B)
    https://www.thisisant.com/resources/ant-message-protocol-and-usage/
    Opens channel 0 in continuous scan mode. Radio is active and receiving 100% of the time. No other
    channels can operate when node is in this mode. Node will pick up any message and match to appropriate
    channel ID. Receives from multiple devices simultaneously.
    
    Network key - (0xB9, 0xA5, 0x21, 0xFB, 0xBD, 0x72, 0xC3, 0x45)
    (https://www.thisisant.com/developer/ant-plus/ant-plus-basics/network-keys)
    Channel Type - (0x40) (slave, unidirectional, receive only channel)
    (https://www.thisisant.com/resources/ant-message-protocol-and-usage/)
    Channel ID - (True -> 0x80) (Enables Channel ID output)
    RSSI - (0x40) (signal strength indication)
    RX Timestamp - (0x20) (timestamp information. generated exactly when message was received by ANT)
    RF frequency - 2457 Hz
    (https://www.thisisant.com/developer/ant-plus/ant-antplus-defined)
    """
    def enableRxScanMode(self,
                         networkKey=ANTPLUS_NETWORK_KEY,
                         channelType=CHANNEL_TYPE_ONEWAY_RECEIVE,
                         frequency: int = 2457,
                         rxTimestamp: bool = True,
                         rssi: bool = True,
                         channelId: bool = True):

        self._init.append(SystemResetMessage())
        self._init.append(SetNetworkKeyMessage(0, networkKey))
        self._init.append(AssignChannelMessage(0, channelType))
        self._init.append(SetChannelIdMessage(0))
        self._init.append(SetChannelRfFrequencyMessage(0, frequency))
        self._init.append(EnableExtendedMessagesMessage())
        self._init.append(LibConfigMessage(rxTimestamp, rssi, channelId))
        self._init.append(OpenRxScanModeMessage())

    """
    Section - 9.5.4.2 - Control Message - Open Channel (0x4B)
    https://www.thisisant.com/resources/ant-message-protocol-and-usage/
    Opens specified channel.
    """
    def enableChannel(self,
                      networkKey=ANTPLUS_NETWORK_KEY,
                      channelType=CHANNEL_TYPE_ONEWAY_RECEIVE,
                      frequency: int = 2457,
                      rxTimestamp: bool = True,
                      rssi: bool = True,
                      channel: int = 0,
                      deviceNumber: int = 0,
                      deviceType: int = 0,
                      searchTimeout: int = 255,
                      channelId: bool = True,
                      channelPeriod: int = 8192):

        self._init.append(SystemResetMessage())
        self._init.append(SetNetworkKeyMessage(channel, networkKey))
        self._init.append(AssignChannelMessage(channel, channelType))
        self._init.append(SetChannelIdMessage(channel, deviceNumber, deviceType))
        self._init.append(SetChannelRfFrequencyMessage(channel, frequency))
        self._init.append(EnableExtendedMessagesMessage())
        self._init.append(LibConfigMessage(rxTimestamp, rssi, channelId))
        self._init.append(SetChannelPeriodMessage(channel, channelPeriod))
        self._init.append(SetSearchTimeoutMessage(channel, searchTimeout))
        self._init.append(OpenChannelMessage(channel))

    def stop(self):
        if self.isRunning():
            self._pump.stop()
            self._pump.join()

    def isRunning(self):
        if self._pump is None:
            return False
        return self._pump.is_alive()

    def getCapabilities(self):
        pass
