import asyncio
from scripts.Bluetooth.BLEScanner import BLEScanner
from scripts.Bluetooth.BLEClient import BLEClient

"""
BLE Listener Class. Used to listen for Wahoo Kickr Bluetooth readings.
"""
class BluetoothListener():
    def __init__(self, loop):
        self.loop = loop
        self.CYCLING_POWER_CHARACTERISTIC_UUID = '00002a63-0000-1000-8000-00805f9b34fb'

    async def listen(self):
        # Discover BLE Devices
        scanner = BLEScanner()
        devices = await scanner.discover(timeout=5)

        # Print BLE Devices Found
        wahooKickrDevice = None

        print('Available BLE Devices: ')
        for device in devices:
            if 'KICKR SNAP' in str(device):
                wahooKickrDevice = device

        if wahooKickrDevice:
            print('Wahoo Kickr Device Found')

        else:
            print('Wahoo Kickr Device Not Found')
            return

        # Connect to Wahoo Kickr Device
        client = BLEClient(wahooKickrDevice.address, self.loop)
        await client.connect(timeout=5)
        connected = await client.is_connected()

        if connected:
            print('Connected to Wahoo Kickr Device')

        else:
            print('Failed to Connect to Wahoo Kickr Device')
            return

        # Retrieve GATT Services
        services = await client.get_services()

        for service in services:
            print("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                print(
                    "\t[Characteristic] {0}: (Handle: {1}) ({2}) | Name: {3}, Value: {4} ".format(
                        char.uuid,
                        char.handle,
                        ",".join(char.properties),
                        char.description,
                        value,
                    )
                )
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    print(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )
            pass

        await client.start_notify(self.CYCLING_POWER_CHARACTERISTIC_UUID, self.cyling_power_measurement)

        await asyncio.sleep(100.0, loop=self.loop)

    def cyling_power_measurement(self, sender, data):
        print("{0}: {1}".format(sender, data))

    def detection_callback(self, *args):
        print(args)
