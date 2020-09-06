from scripts.libAnt.constants import *


class Message:
    def __init__(self, type: int, content: bytes):
        self._type = type
        self._content = content

    def __len__(self):
        return len(self._content)

    def __iter__(self):
        return self._content

    def __str__(self):
        return '({:02X}): '.format(self._type) + ' '.join('{:02X}'.format(x) for x in self._content)

    def checksum(self) -> int:
        chk = MESSAGE_TX_SYNC ^ len(self) ^ self._type
        for b in self._content:
            chk ^= b
        return chk

    def encode(self) -> bytes:
        b = bytearray([MESSAGE_TX_SYNC, len(self), self._type])
        b.extend(self._content)
        b.append(self.checksum())
        return bytes(b)

    @property
    def type(self) -> int:
        return self._type

    @property
    def content(self) -> bytes:
        return self._content


class BroadcastMessage(Message):
    def __init__(self, type: int, content: bytes):
        self.flag = None
        self.deviceNumber = self.deviceType = self.transType = None
        self.rssiMeasurementType = self.rssi = self._rssiThreshold = None
        self.rssi = None
        self.rssiThreshold = None
        self.rxTimestamp = None
        self.channel = None
        self.extendedContent = None

        super().__init__(type, content)

    """
    Standard Message Content: [Channel #, Payload]
    Extended Message Content: [Channel #, Payload, Flag Byte, Device Number, Device Type, Trans Type, 
                               Flag Byte, RSSI, Timestamp]
    """
    def build(self, raw: bytes):
        self._type = MESSAGE_CHANNEL_BROADCAST_DATA
        self.channel = raw[0]
        self._content = raw[1:9]
        if len(raw) > 9:  # Extended message
            self.flag = raw[9]
            self.extendedContent = raw[10:]
            offset = 0
            if self.flag & EXT_FLAG_CHANNEL_ID:
                self.deviceNumber = int.from_bytes(self.extendedContent[:2], byteorder='little', signed=False)
                self.deviceType = self.extendedContent[2]
                self.transType = self.extendedContent[3]
                offset += 4
            if self.flag & EXT_FLAG_RSSI:
                rssi = self.extendedContent[offset:(offset + 3)]
                self.rssiMeasurementType = rssi[0]
                self.rssi = rssi[1]
                self.rssiThreshold = rssi[2]
                offset += 3
            if self.flag & EXT_FLAG_TIMESTAMP:
                self.rxTimestamp = int.from_bytes(self.extendedContent[offset:],
                                                  byteorder='little', signed=False)
        return self

    def checksum(self) -> int:
        pass

    def encode(self) -> bytes:
        pass


"""
Control Message - Reset System (Section 9.5.4.1)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/

**Arguments:** Message ID (0X4A), 0
"""
class SystemResetMessage(Message):
    def __init__(self):
        super().__init__(MESSAGE_SYSTEM_RESET, b'0')


"""
Config Message - Set Network Key (Section 9.5.2.7)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Network Number - Available networks on ANT device. Default network number is 0 (Public Network) (Section - 5.2.5.1) 
Network Key - Unique network identifier (Section - 5.2.5.2)

**Arguments:** Message ID (0x46), Network Number, Network Key
"""
class SetNetworkKeyMessage(Message):
    def __init__(self, channel: int, key: bytes = ANTPLUS_NETWORK_KEY):
        content = bytearray([channel])
        content.extend(key)
        super().__init__(MESSAGE_NETWORK_KEY, bytes(content))


"""
Config Message - Assign Channel (Section 9.5.2.2)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Channel Number - Channel number of assigned channel. Must be less than number of channels supported by device 
Channel Type - Bi-directional (0x00) (Slave/Master), Shared Bi-directional (0x10) (Slave/Master), 
             Slave Receive-Only (0x40), Master Transmit-Only (0x50) (Section - 5.2.1)
Network Number - Available networks on ANT device. Default network number is 0 (Public Network) (Section - 5.2.5.1)
Extended Assign't (optional) - Allows various ANT features to be enabled (Section - 5.2.1.4)
  
**Arguments:** Message ID (0x42), Channel Number, Channel Type, Network Number, Extended Assign't (optional)
"""
class AssignChannelMessage(Message):
    def __init__(self, channel: int, type: int, network: int = 0, extended: int = None):
        content = bytearray([channel, type, network])
        if extended is not None:
            content.append(extended)
        super().__init__(MESSAGE_CHANNEL_ASSIGN, bytes(content))


"""
Config Message - Channel ID (Section 9.5.2.3)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Channel ID - Transmitting device's channel ID (Section - 7.1.1.1)
  Device Number - 16-bit field unique to each device. Typically the serial number for the device (Section - 5.2.3.3)
  Device Type - 8-bit field denoting type of device (device profile) (Section - 5.2.3.1)
  Transmission Type - Transmission characteristics of device (Section - 5.2.3.1)

**Arguments:** Message ID (0x51), Channel Number, Device Number, Device Type ID, Transmission Type
"""
class SetChannelIdMessage(Message):
    def __init__(self, channel: int, deviceNumber: int = 0, deviceType: int = 0, transType: int = 0):
        content = bytearray([channel])
        content.extend(deviceNumber.to_bytes(2, byteorder='big'))
        content.append(deviceType)
        content.append(transType)
        super().__init__(MESSAGE_CHANNEL_ID, bytes(content))


"""
Config Message - Channel RF Frequency (Section 9.5.2.6)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
The operating frequency for the channel. 2457 reserved for ANT+
**Arguments**: Message ID (0x45), Channel Number, RF Frequency
"""
class SetChannelRfFrequencyMessage(Message):
    def __init__(self, channel: int, frequency: int = 2457):
        content = bytes([channel, frequency - 2400])
        super().__init__(MESSAGE_CHANNEL_FREQUENCY, content)


"""
Config Message - Channel Period (Section 9.5.2.4)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Channel Period
**Arguments**: Message ID (0x43), Channel Number, Channel Period (default = 8192 (4 Hz))
"""
class SetChannelPeriodMessage(Message):
    def __init__(self, channel: int, period: int = 8192):
        content = bytearray([channel])
        content.extend(period.to_bytes(2, byteorder='big'))
        super().__init__(MESSAGE_CHANNEL_PERIOD, content)


"""
Config Message - Search Timeout (Section 9.5.2.5)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Search Timeout
**Arguments**: Message ID (0x43), Channel Number, Search Timeout (default = 255 (never timeout))
"""
class SetSearchTimeoutMessage(Message):
    def __init__(self, channel: int, timeout: int = 255):
        content = bytearray([channel, timeout])
        super().__init__(MESSAGE_CHANNEL_PERIOD, content)


"""
Control Message - Open Rx Scan Mode (Section - 9.5.4.5)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Opens channel 0 in continuous scan mode. Radio is active and receiving 100% of the time. No other
channels can operate when node is in this mode. Node will pick up any message and match to appropriate
channel ID. Receives from multiple devices simultaneously.

**Arguments**: Message ID (0x5B), 0, Synchronous Channel Packets Only (Optional)
"""
class OpenRxScanModeMessage(Message):
    def __init__(self):
        super().__init__(OPEN_RX_SCAN_MODE, bytes([0]))


"""
Control Message - Open Channel (Section - 9.5.4.2)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Opens specified channel.

**Arguments**: Message ID (0x4B), channel
"""
class OpenChannelMessage(Message):
    def __init__(self, channel: int):
        super().__init__(MESSAGE_CHANNEL_OPEN, bytes([channel]))


"""
Config Message - Extended Data Message (Section 7.1.1)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Channel ID (0x80) - Transmitting device's channel ID (Section - 7.1.1.1)
  Device Number - 16-bit field unique to each device. Typically the serial number for the device (Section - 5.2.3.3)
  Device Type - 8-bit field denoting type of device (device profile) (Section - 5.2.3.1)
  Transmission Type - Transmission characteristics of device (Section - 5.2.3.1)
  
**Arguments:** Message ID (0x66), 0, Enable
"""
class EnableExtendedMessagesMessage(Message):
    def __init__(self, enable: bool = True):
        content = bytes([0, int(enable)])
        super().__init__(MESSAGE_ENABLE_EXT_RX_MESSAGES, content)


"""
Config Message - Lib Config (Section - 9.5.2.20)
https://www.thisisant.com/resources/ant-message-protocol-and-usage/
Used to extend Rx message. Can pass channel ID, RSSI, and Timestamp information in the extended data byte
Relative order of Rx message is channel ID, RSSI, and Timestamp if all enabled
Channel ID (0x80) - Transmitting device's channel ID (Section - 7.1.1.1)
  Device Number - 16-bit field unique to each device. Typically the serial number for the device (Section - 5.2.3.3)
  Device Type - 8-bit field denoting type of device (device profile) (Section - 5.2.3.1)
  Transmission Type - Transmission characteristics of device (Section - 5.2.3.1)
RSSI (0x40) - Signal strength indication (Section - 7.1.1.2)
  Measurement Type (0x20) - RSSI value units of dBm (Section - 7.1.1.2.1)
  RSSI Value - Integer corresponding to measured RSSI value in dBm (Section - 7.1.1.2.2)
  Threshold Configuration Value - dBm value of the bin (Section - 7.1.1.2.3)
Timestamp (0x20) - Timestamp data (Section - 7.1.1.3)
   Rx Timestamp - The exact time when the message was received by ANT over the air (Section - 7.1.1.3.1)

**Arguments**: Message ID (0x6E), 0, Lib Config [Channel ID, RSSI, Timestamp]
"""
class LibConfigMessage(Message):
    def __init__(self, rxTimestamp: bool = True, rssi: bool = True, channelId: bool = True):
        config = 0
        if rxTimestamp:
            config |= EXT_FLAG_TIMESTAMP
        if rssi:
            config |= EXT_FLAG_RSSI
        if channelId:
            config |= EXT_FLAG_CHANNEL_ID
        super().__init__(MESSAGE_LIB_CONFIG, bytes([0, config]))
