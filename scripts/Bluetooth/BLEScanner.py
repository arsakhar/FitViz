import asyncio
from bleak import BleakScanner

"""
BLE Scanner Class. Inherits from BleakScanner. Used to discover BLE Devices
"""
class BLEScanner(BleakScanner):
    def __init__(self):
        super().__init__()

    """
    Discover returns a list of detected Bluetooth LE devices.
    More specifically, it returns a list of instances of BLEDevice class.
    Has attributes address, name, details, rssi, and metadata (uuids, manufacturer_data)
    https://bleak.readthedocs.io/en/latest/api.html#bleak.backends.device.BLEDevice
    """
    async def discover(self, timeout=5):
        await self.start()
        await asyncio.sleep(timeout)
        await self.stop()
        devices = await self.get_discovered_devices()

        return devices
