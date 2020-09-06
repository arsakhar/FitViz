# FitViz
## Health and fitness monitoring client for fitness enthusiasts and gamers

![FitViz Banner](https://raw.githubusercontent.com/uwburn/cardia/master/Readme/cardia1small.png)

_Developed by Ashwin Sakhare_

FitViz is a monitoring client designed for fitness enthusiasts. It supports real-time visualization and tracking of health and fitness data sent from ANT+ devices. FitViz also provides networking capabilities allowing game developers to easily integrate ANT+ devices, such as bike trainers and heart rate monitors, into their own game.

- - - -

### About ANT+

<a href="https://www.thisisant.com/" target="_blank">ANT+</a> is a wireless sensor network technology that allows you to moniter data broadcast from ANT+ capable devices. Fitness equipment, bike trainers, heart rate monitors, and blood pressure monitors are just a few of the many devices supported within the ANT+ ecosystem. Data broadcast from ANT+ devices is standardized based on the type of data being sent. ANT+ refers to a data type as a <a href="https://www.thisisant.com/developer/ant-plus/device-profiles" target="_blank">device profile</a>. An ANT+ device can broadcast data associated with multiple device profiles. For example, the Wahoo Kickr Snap broadcast's Bicycle Power and Fitness Equipment data.

- - - -

### Support Devices
 
FitViz currently support the following device profiles:
* Heart Rate
* Bicycle Cadence
* Bicycle Speed
* Bicycle Speed and Cadence
* Bicycle Power
* Fitness Equipment

- - - -

### Installation

FitViz was written using Python 3.8. To run it from an IDE, the following dependencies are required: PyQt5 and Pyusb. A distributable, FitViz.exe, is included and can be executed as a standalone program. FitViz has only been tested on Windows 10. An ANT+ usb dongle is required for most PC's to connect to ANT+ devices. I used the <a href="https://www.wahoofitness.com/devices/bike-trainers/usb-ant-kit" target="_blank">Wahoo USB ANT+ kit</a> for testing.

- - - -

### User guide

There are 3 primary tabs on the client GUI: Networking, View, and Logging.

#### Networking

![Networking Tab](https://raw.githubusercontent.com/arsakhar/fitviz/master/readme/networking.png)

The Networking tab is used to connect to ANT+ devices. 

* Click on the Run button under Network Controls to scan for ANT+ devices. ANT+ devices identified during the scan period (5 seconds) are displayed in the Broadcasting Devices panel. If ANT+ devices are identified, the network driver continues to listen indefinitely for incoming ANT+ messages.
* If a device is unknown, it will be named "Unknown Device <device number>" in the Broadcasting Devices panel. You can double click on the device entry in the panel to rename the device. Note: the name change will not take effect until the next ANT+ session.
* Once an ANT+ session is started, it will continue to run indefinitely. An ANT+ session can be closed by selecting the Stop button under Network Controls.
* The Reset button can be used to reset any measurement values that accumulate over time. For example, some ANT+ messages associated with a Bicycle Trainer included distance traveled and elapsed time, which are accumulated measurements over time. The reset button will set those measurements to 0.
* The Network Statistics panel displays basic ANT+ network statistics including: # messages received, # ANT+ devices broadcasting, # device profiles received, and message frequency.

#### View

!View Tab](https://raw.githubusercontent.com/arsakhar/fitviz/master/readme/view.png)

The Logging tab is used to visualize measurement data from ANT+ devices. There are 4 viewing panels allowing for up to 4 measurements to be viewed concurrently in real-time.

* Select a device from the Devices dropdown box.
* Select a profile from the Profiles box.
* Select a data page from the Data Pages box
* Select a page measurement from the Page Measurements box.

The measurement will be displayed on a gauge or LCD number UI depending on the type of measurement. Generally speaking, accumulated measurements such as elapsed time and distance traveled will be displayed as an LCD number while measurements within a typical range will be displayed on the gauge UI.

#### Logging

![Logging Tab](https://raw.githubusercontent.com/arsakhar/fitviz/master/readme/csv.png)

There are 2 logging options: UDP and CSV. CSV logging is simply writing data to a user-specified CSV file. For UDP logging, data is written to the specified ip address and port. The intent behind UDP is to allow for real-time data transfer to another program or device. In both cases, data is written each time a message is received.

* First, begin by adding the measurements you would like to track.
* For CSV logging, set the filename and select Start to begin logging.
* For UDP logging, set the port and ip address and select Start to begin logging.
* UDP data is delivered as a byte array of the following format: [measurement 1 value; measurement 2 value; measurement 3 value; measurement 4 value; ...]

- - - -

### About the code
The idea behind this project was to provide a standalone PC application that could allow my research lab to monitor and interface with a Wahoo Kickr Snap bike trainer. In particular, we were interested in real-time measurements of speed and power to use the Kickr as an input controller for a VR game we were developing. And so my journey began to create a program that can interface with ANT+ devices.

An external python package, <a href="https://github.com/half2me/libant target="_blank">LibAnt</a>, was modified and used for the ANT+ backend communication. The inspiration for the GUI design was based on <a href="https://github.com/Wanderson-Magalhaes/Simple_PySide_Base target="_blank">Simple Pyside Base</a>. Inspiration for UDP logging was provided by <a href="https://github.com/uwburn/cardia target="_blank">Cardia</a>.

The app currently only supports a limited number of ANT+ device profiles. However, my hope is to continue to expand on this slowly over time. Tis is an alpha release and there are likely several bugs as I haven't yet had a chance to rigorously test everything.

- - - -

### Changelog
* v1.0.0 alpha (2020-09-05)
  * Initial release