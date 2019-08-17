# Sphero Raspberry-Pi Python SDK

This package provides two ways with interacting with the Sphero API Service:
- Asynchronous using the asyncio library (Advanced)
- Observer-based using an event based design (Easier)

Please check out our `getting_started` directory for samples using both versions.

### Raspberry-pi configuration:

We recommend grabbing a pre-configured image of Rasbian Stretch that already has our dependencies pre-installed.
It can be 

We use the [Raspbian-Stretch (2018-11-15 release)](https://downloads.raspberrypi.org/raspbian/images/raspbian-2018-11-15/) to develop and test our SDK. While there are multiple ways to configure a raspberry-pi in order to use our SDK,   
our go-to approach is to clone a pre-configured image onto a 16GB micro SD card.  

Grab our cloned image from here (they're ~15GB) :
- [Image for Mac users](https://drive.google.com/open?id=1NgTbpGDMIXSNoYihaXbX4I-_8LAW3BBv)
- [Image for Windows users](https://drive.google.com/open?id=1PdI8XN_EZpAd72o6kXaYYg41QK9FzD-K) 

Here are a couple of helpful links on how to clone those images onto an micro SD card:
- [Instructions for Mac OS](https://computers.tutsplus.com/articles/how-to-clone-raspberry-pi-sd-cards-using-the-command-line-in-os-x--mac-59911)
- [Instructions for Windows](https://computers.tutsplus.com/articles/how-to-clone-your-raspberry-pi-sd-cards-with-windows--mac-59294)

If you'd rather set up a pi manually, you can install our dependencies in running the shell script in the found in the `pi_dependencies` directory.

#### Additional notes:
- We've developed and tested using python 3.5.3
- Be sure to enable the serial port (found in raspberry-pi config menu)
- Be sure to disable the serial console. (also found in the same menu)