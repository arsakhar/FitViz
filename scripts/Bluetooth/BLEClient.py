import asyncio
from bleak import BleakClient


"""
BLE Client Class. Inherits from BleakClient.
"""
class BLEClient(BleakClient):
    def __init__(self, address, loop):
        super().__init__(address, loop)

    """
    Connect to a specified device. **kwargs specifies timeout period
    """
    def connect(self, **kwargs):
        return super().connect(**kwargs)

    """
    Check if connection is active.
    """
    def is_connected(self):
        return super().is_connected()

    """
    Retrieve GATT Services (https://www.bluetooth.com/specifications/gatt/services/)
    """
    def get_services(self):
        return super().get_services()