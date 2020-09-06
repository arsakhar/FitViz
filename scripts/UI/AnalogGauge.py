from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QSize, QPoint, QPointF, QTimer, QRect
from PyQt5.QtGui import QFont, QColor, QPolygon, QPen, QPolygonF, QPainter, QFontMetrics, QConicalGradient
import math


class AnalogGaugeWidget(QWidget):
    gaugeValueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(AnalogGaugeWidget, self).__init__(parent)

        self.useTimerEvent = False

        self.initUI()

    def initUI(self):
        # Color of needle
        self.setNeedleColor(50, 50, 50, 255)

        # Color of needle hub
        self.setNeedleHubColor(50, 50, 50, 255)

        # Color of gauge values
        self.setGaugeValuesColor(255, 255, 255, 255)

        # Color of LCD value
        self.setDigitalValueColor(255, 255, 255, 255)

        # Gauge needle object
        self.needle = QObject
        self.setNeedleStyle([QPolygon([
            QPoint(4, 4),
            QPoint(-4, 4),
            QPoint(-3, -120),
            QPoint(0, -126),
            QPoint(3, -120)
        ])])

        # minimum gauge value
        self.minGaugeValue = 0

        # maximum gauge value
        self.maxGaugeValue = 500

        # current gauge value
        self.gaugeValue = self.minGaugeValue

        # gauge value units
        self.gaugeValueUnits = ''

        # outer radius of gauge
        self.gaugeOuterRadius = 1

        # inner radius of gauge
        self.gaugeInnerRadius = 0.95

        # orientation of gauge
        self.gaugeRotation = 135

        # number of degrees to draw gauge (360 is a complete circle)
        self.gaugeArcAngle = 270

        # number of gauge values
        self.setGaugeValueMajorAxisCount(10)

        # number of ticks between gauge values
        self.gaugeValueMinorAxisCount = 5

        self.pen = QPen(QColor(0, 0, 0))
        self.font = QFont('Decorative', 20)

        self.gaugeColors = []
        self.setGaugeColors([[.00, Qt.red],
                             [.1, Qt.yellow],
                             [.15, Qt.green],
                             [1, Qt.transparent]])

        # gauge value font family and font size
        self.setGaugeValuesEnabled(True)
        self.gaugeValueFont = "Decorative"
        self.initGaugeValueFontSize = 15
        self.gaugeValueFontSize = self.initGaugeValueFontSize

        # digital value font family and font size
        self.digitalValueEnabled = True
        self.digitalValueFontName = "Decorative"
        self.initDigitalValueFontSize = 40
        self.digitalValueUnitsFontSize = 15
        self.digitalValueFontSize = self.initDigitalValueFontSize
        self.digitalValueRadius = 0.7

        self.setGaugeColorBarsEnabled(True)
        self.setGaugeAnnulusFilledEnabled(True)

        self.needleHubEnabled = True
        self.gaugeMinorAxisMarkerEnabled = True
        self.gaugeMajorAxisMarkerEnabled = True

        self.needleSize = 0.8
        self.needleEnabled = True

        self.update()

        self.resizeGauge()

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(300, 300))
        self.setMaximumSize(QSize(600, 600))
        self.setBaseSize(QSize(300, 300))

    def resizeGauge(self):
        if self.width() <= self.height():
            self.widgetDiameter = self.width()
        else:
            self.widgetDiameter = self.height()

        self.setNeedleStyle([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, - self.widgetDiameter / 2 * self.needleSize),
            QPoint(0, - self.widgetDiameter / 2 * self.needleSize - 6),
            QPoint(2, - self.widgetDiameter / 2 * self.needleSize)
        ])])

        self.gaugeValueFontSize = self.initGaugeValueFontSize * self.widgetDiameter / 400
        self.digitalValueFontSize = self.initDigitalValueFontSize * self.widgetDiameter / 400

    def setNeedleStyle(self, design):
        self.needle = []
        for i in design:
            self.needle.append(i)

        self.update()

    def updateGaugeValue(self, value):
        if value <= self.minGaugeValue:
            self.gaugeValue = self.minGaugeValue
        elif value >= self.maxGaugeValue:
            self.gaugeValue = self.maxGaugeValue
        else:
            self.gaugeValue = value

        self.gaugeValueChanged.emit(int(value))

        self.update()

    ###############################################################################################
    # Set Methods
    ###############################################################################################
    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        self.needleColor = QColor(R, G, B, Transparency)

        self.update()

    def setGaugeValuesColor(self, R=50, G=50, B=50, Transparency=255):
        self.gaugeValuesColor = QColor(R, G, B, Transparency)

        self.update()

    def setDigitalValueColor(self, R=50, G=50, B=50, Transparency=255):
        self.digitalValueColor = QColor(R, G, B, Transparency)

        self.update()

    def setNeedleHubColor(self, R=50, G=50, B=50, Transparency=255):
        self.needleHubColor = QColor(R, G, B, Transparency)

        self.update()

    def setNeedleEnabled(self, enable=True):
        self.needleEnabled = enable

        self.update()

    def setGaugeValuesEnabled(self, enable=True):
        self.gaugeValuesEnabled = enable

        self.update()

    def setGaugeColorBarsEnabled(self, enable=True):
        self.GaugeColorBarsEnabled = enable

        self.update()

    def setDigitalValueEnabled(self, enable=True):
        self.digitalValueEnabled = enable

        self.update()

    def setNeedleHubEnabled(self, enable=True):
        self.needleHubEnabled = enable

        self.update()

    def setGaugeAnnulusFilledEnabled(self, enable=True):
        self.gaugeAnnulusEnabled = enable

        self.update()

    def setGaugeMajorAxisEnabled(self, enable=True):
        self.gaugeMajorAxisMarkerEnabled = enable

        self.update()

    def setGaugeMinorAxisEnabled(self, enable=True):
        self.gaugeMinorAxisMarkerEnabled = enable

        self.update()

    def setGaugeValueMajorAxisCount(self, count):
        if count < 1:
            count = 1

        self.gaugeValueMajorAxisCount = count

        self.update()

    def setGaugeValueUnits(self, unit):
        self.gaugeValueUnits = unit

    def setMinGaugeValue(self, min):
        if self.gaugeValue < min:
            self.gaugeValue = min

        if min >= self.maxGaugeValue:
            self.minGaugeValue = self.maxGaugeValue - 1
        else:
            self.minGaugeValue = min

        self.update()

    def setMaxGaugeValue(self, max):
        if self.gaugeValue > max:
            self.gaugeValue = max

        if max <= self.minGaugeValue:
            self.maxGaugeValue = self.minGaugeValue + 1
        else:
            self.maxGaugeValue = max

        self.update()

    def setGaugeRotation(self, value):
        self.gaugeRotation = value

        self.update()

    def setGaugeArcAngle(self, value):
        self.gaugeArcAngle = value

        self.update()

    def setGaugeOuterRadius(self, value):
        self.gaugeOuterRadius = float(value) / 1000

        self.update()

    def setGaugeInnerRadius(self, value):
        self.gaugeInnerRadius = float(value) / 1000

        self.update()

    def setGaugeColors(self, colorArray):
        if 'list' in str(type(colorArray)):
            self.gaugeColors = colorArray
        elif colorArray == None:
            self.gaugeColors = [[.0, Qt.transparent]]
        else:
            self.gaugeColors = [[.0, Qt.transparent]]

        self.update()

    ###############################################################################################
    # Get Methods
    ###############################################################################################
    def getMaxGaugeValue(self):
        return self.maxGaugeValue

    ###############################################################################################
    # Painter
    ###############################################################################################
    def drawGauge(self, outerRadius, innerRadius, start, length):
        gauge = QPolygonF()

        n = 360  # angle steps size for full circle

        w = 360 / n  # angle per step

        x = 0
        y = 0

        if not self.GaugeColorBarsEnabled:
            length = int(round((length / (self.maxGaugeValue - self.minGaugeValue)) *
                               (self.gaugeValue - self.minGaugeValue)))

        # add the points of polygon
        for i in range(length + 1):
            t = w * i + start
            x = outerRadius * math.cos(math.radians(t))
            y = outerRadius * math.sin(math.radians(t))
            gauge.append(QPointF(x, y))

        # create inner circle line from "start + length"-angle to "start"-angle
        for i in range(length + 1):  # add the points of polygon
            t = w * (length - i) + start
            x = innerRadius * math.cos(math.radians(t))
            y = innerRadius * math.sin(math.radians(t))
            gauge.append(QPointF(x, y))

        # close outer line
        gauge.append(QPointF(x, y))
        return gauge

    def drawGaugeAnnulus(self, outlinePenWith=0):
        if not self.gaugeColors == None:
            gaugeAnnulus = QPainter(self)
            gaugeAnnulus.setRenderHint(QPainter.Antialiasing)
            gaugeAnnulus.translate(self.width() / 2, self.height() / 2)

            gaugeAnnulus.setPen(Qt.NoPen)

            self.pen.setWidth(outlinePenWith)
            if outlinePenWith > 0:
                gaugeAnnulus.setPen(self.pen)

            coloredScalePolygon = self.drawGauge(
                ((self.widgetDiameter / 2) - (self.pen.width() / 2)) * self.gaugeOuterRadius,
                (((self.widgetDiameter / 2) - (self.pen.width() / 2)) * self.gaugeInnerRadius),
                self.gaugeRotation, self.gaugeArcAngle)

            gradient = QConicalGradient(QPointF(0, 0), - self.gaugeArcAngle - self.gaugeRotation +
                                    - 1)

            for eachcolor in self.gaugeColors:
                gradient.setColorAt(eachcolor[0], eachcolor[1])

            gaugeAnnulus.setBrush(gradient)
            gaugeAnnulus.drawPolygon(coloredScalePolygon)

    ###############################################################################################
    # Gauge Axis Markers
    ###############################################################################################
    def drawGaugeMajorAxisMarkers(self):
        myPainter = QPainter(self)
        myPainter.setRenderHint(QPainter.Antialiasing)
        myPainter.translate(self.width() / 2, self.height() / 2)

        self.pen = QPen(QColor(0, 0, 0, 255))
        self.pen.setWidth(2)

        myPainter.setPen(self.pen)
        myPainter.rotate(self.gaugeRotation)

        stepsSize = (float(self.gaugeArcAngle) / float(self.gaugeValueMajorAxisCount))
        scaleLineOuterStart = self.widgetDiameter / 2
        scaleLineLength = (self.widgetDiameter / 2) - (self.widgetDiameter / 20)

        for i in range(self.gaugeValueMajorAxisCount + 1):
            myPainter.drawLine(scaleLineLength, 0, scaleLineOuterStart, 0)
            myPainter.rotate(stepsSize)

    def drawGaugeValues(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        font = QFont(self.gaugeValueFont, self.gaugeValueFontSize)
        fm = QFontMetrics(font)

        penShadow = QPen()

        penShadow.setBrush(self.gaugeValuesColor)
        painter.setPen(penShadow)

        gaugeValueRadiusFactor = 0.8
        gaugeValueRadius = self.widgetDiameter / 2 * gaugeValueRadiusFactor

        scalePerDiv = int((self.maxGaugeValue - self.minGaugeValue) / self.gaugeValueMajorAxisCount)

        angleDistance = (float(self.gaugeArcAngle) / float(self.gaugeValueMajorAxisCount))

        for i in range(self.gaugeValueMajorAxisCount + 1):
            text = str(int(self.minGaugeValue + scalePerDiv * i))

            w = fm.width(text) + 1
            h = fm.height()

            painter.setFont(QFont(self.gaugeValueFont, self.gaugeValueFontSize))
            angle = angleDistance * i + float(self.gaugeRotation)

            x = gaugeValueRadius * math.cos(math.radians(angle))
            y = gaugeValueRadius * math.sin(math.radians(angle))

            text = [x - int(w / 2), y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]

            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def drawGaugeMinorAxisMarkers(self):
        myPainter = QPainter(self)
        myPainter.setRenderHint(QPainter.Antialiasing)
        myPainter.translate(self.width() / 2, self.height() / 2)
        myPainter.setPen(Qt.black)
        myPainter.rotate(self.gaugeRotation)

        stepsSize = (float(self.gaugeArcAngle) / float(self.gaugeValueMajorAxisCount * self.gaugeValueMinorAxisCount))
        scaleLineOuterStart = self.widgetDiameter / 2
        scaleLineLength = (self.widgetDiameter / 2) - (self.widgetDiameter / 40)

        for i in range((self.gaugeValueMajorAxisCount * self.gaugeValueMinorAxisCount) + 1):
            myPainter.drawLine(scaleLineLength, 0, scaleLineOuterStart, 0)
            myPainter.rotate(stepsSize)

    def drawDigitalValue(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        font = QFont(self.digitalValueFontName, self.digitalValueFontSize)
        fm = QFontMetrics(font)

        penShadow = QPen()
        penShadow.setBrush(self.digitalValueColor)
        painter.setPen(penShadow)

        digitalValueRadius = self.widgetDiameter / 2 * self.digitalValueRadius

        text = str(int(self.gaugeValue))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.digitalValueFontName, self.digitalValueFontSize))

        angleEnd = float(self.gaugeRotation + self.gaugeArcAngle - 360)
        angle = (angleEnd - self.gaugeRotation) / 2 + self.gaugeRotation

        x = digitalValueRadius * math.cos(math.radians(angle))
        y = digitalValueRadius * math.sin(math.radians(angle))

        offset = 20 if self.gaugeValueUnits else 0

        text = [x - int(w / 2) - offset, y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

        self.drawDigitalValueUnits()

    def drawDigitalValueUnits(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        font = QFont(self.digitalValueFontName, self.digitalValueUnitsFontSize)
        fm = QFontMetrics(font)

        penShadow = QPen()
        penShadow.setBrush(self.digitalValueColor)
        painter.setPen(penShadow)

        digitalValueRadius = self.widgetDiameter / 2 * self.digitalValueRadius

        text = self.gaugeValueUnits
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.digitalValueFontName, self.digitalValueUnitsFontSize))

        angleEnd = float(self.gaugeRotation + self.gaugeArcAngle - 360)
        angle = (angleEnd - self.gaugeRotation) / 2 + self.gaugeRotation

        x = digitalValueRadius * math.cos(math.radians(angle))
        y = digitalValueRadius * math.sin(math.radians(angle))

        text = [x - int(w / 2) + 20, y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])

    def drawNeedleHub(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.needleHubColor)

        painter.drawEllipse(int(-diameter / 2), int(-diameter / 2), int(diameter), int(diameter))

    def drawNeedle(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.needleColor)
        painter.rotate(((self.gaugeValue - self.minGaugeValue) * self.gaugeArcAngle /
                        (self.maxGaugeValue - self.minGaugeValue)) + 90 + self.gaugeRotation)

        painter.drawConvexPolygon(self.needle[0])

    ###############################################################################################
    # Events
    ###############################################################################################
    def resizeEvent(self, event):
        self.resizeGauge()

    def paintEvent(self, event):
        # Main Drawing Event: Executed on every change

        # draw gauge annulus
        if self.gaugeAnnulusEnabled:
            self.drawGaugeAnnulus()

        # draw gauge axis markers
        if self.gaugeMinorAxisMarkerEnabled:
            self.drawGaugeMinorAxisMarkers()
        if self.gaugeMajorAxisMarkerEnabled:
            self.drawGaugeMajorAxisMarkers()

        # draw gauge values
        if self.gaugeValuesEnabled:
            self.drawGaugeValues()

        # display digital value
        if self.digitalValueEnabled:
            self.drawDigitalValue()

        # draw needle
        if self.needleEnabled:
            self.drawNeedle()

        # draw needle hub
        if self.needleHubEnabled:
            self.drawNeedleHub(diameter=(self.widgetDiameter / 6))
