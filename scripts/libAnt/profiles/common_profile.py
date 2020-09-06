from scripts.libAnt.core import lazyproperty
from scripts.libAnt.profiles.profile import ProfileMessage

MANUFACTURER_INFORMATION_DATA = 0x50
PRODUCT_INFORMATION_DATA = 0x51


class CommonProfile:
    def __init__(self):
        self.dataPages = {
            MANUFACTURER_INFORMATION_DATA: ManufacturerInformation,
            PRODUCT_INFORMATION_DATA: ProductInformation,
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
            dataPageMessage = CommonProfileMessage(msg, previous)

        return dataPageMessage


class CommonProfileMessage(ProfileMessage):
    """ Message from Common Data """

    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    @lazyproperty
    def dataPageNumber(self):
        """
        :return: Data Page Number (int)
        """
        return self.msg.content[0]


class ManufacturerInformation(CommonProfileMessage):
    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    def __str__(self):
        ret = '{} Hardware Revision: {:d}'.format(super().__str__(), self.hwRevision)
        ret += ' Manufacturer ID: {:d}'.format(self.manufacturerID)
        ret += ' Model Number: {:d}'.format(self.modelNumber)

        return ret

    @lazyproperty
    def hwRevision(self):
        """
        :return: Hardware Revision
        """
        return self.msg.content[3]

    @lazyproperty
    def manufacturerID(self):
        """
        :return: Manufacturer ID
        """
        return (self.msg.content[5] << 8) | self.msg.content[4]

    @lazyproperty
    def modelNumber(self):
        """
        :return: Model Number
        """
        return (self.msg.content[7] << 8) | self.msg.content[6]


class ProductInformation(CommonProfileMessage):
    def __init__(self, msg, previous):
        super().__init__(msg, previous)

    def __str__(self):
        ret = '{} Software Revision (Supplemental): {:d}'.format(super().__str__(), self.swRevisionSupplemental)
        ret += ' Software Revision (Main): {:d}'.format(self.swRevisionMain)

        return ret

    @lazyproperty
    def swRevisionSupplemental(self):
        """
        :return: Software Revision (Supplemental)
        """
        return self.msg.content[2]

    @lazyproperty
    def swRevisionMain(self):
        """
        :return: Software Revision (Main)
        """
        return self.msg.content[3]
