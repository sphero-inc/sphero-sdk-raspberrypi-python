#!/bin/bash

# Ask whether the UART is enabled, and give the user a chance to fix it if needed.
while true; do
    read -ep $'By default, the RVR SDK uses the UART on /dev/ttys0 to communicate with RVR.\nDo you have Serial Port enabled and Serial Shell disabled in Raspberry Pi Configuration?\n(y/n):' yn
    case $yn in
        [Yy]* ) exit;;
        [Nn]* ) 
        read -p $'Would you like to open the command line raspi-config tool now to change these settings?\nYou can do this at any time with \'sudo raspi-config\'\n(y/n):' yn2
        case $yn2 in 
                [Yy]* ) sudo raspi-config; break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac 
        break;;
        * ) echo "Please answer yes or no.";;
    esac
done