# FitViz
## ANT+ Health and Fitness Monitoring Client

![FitViz Banner](readme/Logo.PNG?raw=true)

_Developed by Ashwin Sakhare_

FitViz is a monitoring client designed for fitness enthusiasts and gamers. It supports real-time visualization and tracking of health and fitness data sent from ANT+ devices. FitViz also provides networking capabilities allowing game developers to easily integrate ANT+ devices, such as bike trainers and heart rate monitors, into their own game.

- - - -

### About ANT+

<a href="https://www.thisisant.com/" target="_blank">ANT+</a> is a wireless sensor network technology that allows you to moniter data broadcast from ANT+ capable devices. Fitness equipment, bike trainers, heart rate monitors, and blood pressure monitors are just a few of the many devices supported within the ANT+ ecosystem. Data broadcast from ANT+ devices is standardized based on the type of data being sent. ANT+ refers to a data type as a <a href="https://www.thisisant.com/developer/ant-plus/device-profiles" target="_blank">device profile</a>. An ANT+ device can broadcast data associated with multiple device profiles. For example, the Wahoo Kickr Snap broadcasts bicycle power and fitness equipment data.

- - - -

### Supported Devices
 
FitViz currently support the following device profiles:
* Heart Rate
* Bicycle Cadence
* Bicycle Speed
* Bicycle Speed & Cadence
* Bicycle Power
* Fitness Equipment

- - - -

### Installation

FitViz was written in Python (v3.8.5). To run it from an IDE, the following dependencies are required: PyQt5 and Pyusb. A distributable, FitViz.exe, is also included and can be executed as a standalone program. The distributable has only been tested on Windows 10 Pro (10.0.18363 Build 18363). An ANT+ usb dongle is required for most PC's to connect to ANT+ devices. I used the <a href="https://www.wahoofitness.com/devices/bike-trainers/usb-ant-kit" target="_blank">Wahoo USB ANT+ kit</a> for testing.

- - - -

### User guide

There are 3 primary tabs on the client GUI: Networking, View, and Logging.

#### Networking

![Networking Tab](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/Networking.PNG)

The _Networking_ tab is used to connect to ANT+ devices. 

* Select _Run_ under _Network Controls_ to scan for ANT+ devices. ANT+ devices identified during the scan period (5 seconds) are displayed under _Broadcasting Devices_. If ANT+ devices are identified, the network driver continues to listen indefinitely for incoming ANT+ messages.
* If a device is unknown, it will be named "Unknown Device <device number>". You can double click on the device entry under _Broadcasting Devices_ to rename the device. The name change will not take effect until the ANT+ session is restarted.
* Once an ANT+ session is started, it will continue to run indefinitely. An ANT+ session can be closed by selecting _Stop_ under Network Controls.
* _Reset_ can be used to reset measurement values that accumulate over time. For example, some ANT+ messages associated with a Bicycle Trainer included distance traveled and elapsed time, which are accumulated measurements. _Reset_ will set those measurement values to 0.
* _Network Statistics_ displays basic ANT+ network statistics including: # messages received, # ANT+ devices broadcasting, # device profiles received, and message frequency.

#### View

![View Tab](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/View.PNG)

The _View_ tab is used to visualize measurement data from ANT+ devices. There are 4 viewing panels allowing for up to 4 measurements to be viewed concurrently in real-time.

* Select a device from the _Devices_ dropdown box.
* Select a profile from the _Profiles_ box.
* Select a data page from the _Data Pages_ box.
* Select a page measurement from the _Page Measurements_ box.

The measurement will be displayed via a gauge or LCD number depending on the type of measurement. Generally speaking, accumulated measurements will be displayed as an LCD number while measurements that fall within a range will be displayed via the gauge.

#### Logging

![Logging Tab](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/CSV.PNG)

The _Logging_ tab is used to log measurement data.

There are 2 logging options: UDP and CSV. CSV logging is simply writing data to a user-specified CSV file. For UDP logging, data is written to the user-specified ip address and port. The intent behind UDP is to allow for real-time data transfer to another program or device. In both cases, data is written each time a message is received.

* First, begin by adding the measurements you would like to track.
* For CSV logging, set the filename and select _Start_ to begin logging.
* For UDP logging, set the _Port_ and _IP Address_ select _Start_ to begin logging.
* UDP data is delivered as a byte array of the following format: [measurement 1 value; measurement 2 value; measurement 3 value; measurement 4 value; ...]

- - - -

### About

The idea behind this project was to provide a standalone PC application that could allow my research lab to monitor and interface with a Wahoo Kickr Snap bike trainer. In particular, we were interested in real-time measurements of speed and power to use the Kickr as an input controller for a VR game we were developing. And so my journey began to create a program that can interface with ANT+ devices.

The app currently only supports a limited number of ANT+ device profiles. However, my hope is to continue to expand on this slowly over time. This is an alpha release and I haven't performed rigorous testing yet so there are likely a number of bugs to fix. If you a spot a bug, feel free to post it under Issues.

- - - -

### ToDo

- Add bluetooth connection capabilities
- Add device profiles

- - - -

### Changelog

* v1.0.0 alpha (2020-09-05)
  * Initial release
  
- - - -

### Acknowledgements

FitViz would not be possible without liberal imports of PyQt5, Pyusb and LibAnt. <a href="https://github.com/half2me/libant" target="_blank">LibAnt</a> was modified and used for the ANT+ backend communication. The inspiration for the GUI design was based on <a href="https://github.com/Wanderson-Magalhaes/Simple_PySide_Base" target="_blank">Simple Pyside Base</a>. The gauge UI was adapted from <a href="https://github.com/StefanHol/AnalogGaugeWidgetPyQt" target="_blank">Analog Gauge Widget PyQt</a>
