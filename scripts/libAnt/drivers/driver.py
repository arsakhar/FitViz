import time
from abc import abstractmethod
from queue import Empty
from threading import Lock

from scripts.libAnt.constants import MESSAGE_TX_SYNC
from scripts.libAnt.loggers.logger import Logger
from scripts.libAnt.message import Message


class DriverException(Exception):
    pass


class Driver:
    """
    The driver provides an interface to read and write raw data to and from an ANT+ capable hardware device
    """

    def __init__(self, logger: Logger = None):
        self._lock = Lock()
        self._logger = logger
        self._openTime = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def isOpen(self) -> bool:
        with self._lock:
            return self._isOpen()

    def open(self) -> None:
        with self._lock:
            if not self._isOpen():
                self._openTime = time.time()
                if self._logger is not None:
                    self._logger.open()
                self._open()

    def close(self) -> None:
        with self._lock:
            if self._isOpen:
                self._close()
                if self._logger is not None:
                    self._logger.close()

    def reOpen(self) -> None:
        with self._lock:
            if self._isOpen():
                self._close()
            self._open()

    """
    Message Structure (Section 7.1)
    https://www.thisisant.com/resources/ant-message-protocol-and-usage/
    Message Components: [Sync, Msg Length, Msg ID, Message Content, Checksum]
    """
    def read(self, timeout=None) -> Message:
        if not self.isOpen():
            raise DriverException("Device is closed")

        with self._lock:
            while True:
                try:
                    # Byte 0 is Sync
                    sync = self._read(1, timeout=timeout)[0]
                    if sync is not MESSAGE_TX_SYNC:
                        continue

                    # Byte 1 is Message length
                    length = self._read(1, timeout=timeout)[0]

                    # Byte 2 is Message ID (data type)
                    type = self._read(1, timeout=timeout)[0]

                    # Bytes 3..N+2 are Message Content
                    data = self._read(length, timeout=timeout)

                    # Last byte is Checksum
                    chk = self._read(1, timeout=timeout)[0]
                    msg = Message(type, data)

                    if self._logger:
                        logMsg = bytearray([sync, length, type])
                        logMsg.extend(data)
                        logMsg.append(chk)

                        self._logger.log(bytes(logMsg))

                    if msg.checksum() == chk:
                        return msg
                except IndexError:
                    raise Empty

    def write(self, msg: Message) -> None:
        if not self.isOpen():
            raise DriverException("Device is closed")

        with self._lock:
            self._write(msg.encode())

    def abort(self) -> None:
        self._abort()

    @abstractmethod
    def _isOpen(self) -> bool:
        pass

    @abstractmethod
    def _open(self) -> None:
        pass

    @abstractmethod
    def _close(self) -> None:
        pass

    @abstractmethod
    def _read(self, count: int, timeout=None) -> bytes:
        pass

    @abstractmethod
    def _write(self, data: bytes) -> None:
        pass

    @abstractmethod
    def _abort(self) -> None:
        pass