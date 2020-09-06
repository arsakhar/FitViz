import xml.etree.cElementTree as ET
from pathlib import Path

from scripts.Helper.Resources import *

class XMLWriter:
    def __init__(self):
        pass

    def addDevice(self, name, number):
        xmlFile = Path('xml/devices.xml')

        if not xmlFile.is_file():
            root = ET.Element('devices')
            device = ET.SubElement(root, 'device', id='1')

            ET.SubElement(device, 'name').text = str(name)
            ET.SubElement(device, 'number').text = str(number)

            tree = ET.ElementTree(root)
            tree.write(resource_path('xml/devices.xml'))

        else:
            tree = ET.parse(xmlFile)
            root = tree.getroot()

            devices = root.findall('device')

            deviceIDs = []
            for device in devices:
                _id = int(device.attrib['id'])
                _name = device.find('name').text
                _number = int(device.find('number').text)

                if number == _number:
                    device.find('name').text = str(name)

                    tree.write(resource_path('xml/devices.xml'))

                    return

                deviceIDs.append(_id)

            id = deviceIDs[-1] + 1
            device = ET.SubElement(root, 'device', id=str(id))

            ET.SubElement(device, 'name').text = str(name)
            ET.SubElement(device, 'number').text = str(number)

            tree.write('xml/devices.xml')

class XMLReader:
    def __init__(self):
        pass

    def getDeviceNumber2Name(self):
        deviceNumber2Name = {}

        xmlFile = Path(resource_path('xml/devices.xml'))

        if not xmlFile.is_file():
            return {}

        else:
            tree = ET.parse(xmlFile)
            root = tree.getroot()

            devices = root.findall('device')

            for device in devices:
                name = device.find('name').text
                number = int(device.find('number').text)

                deviceNumber2Name[number] = name

            return deviceNumber2Name
