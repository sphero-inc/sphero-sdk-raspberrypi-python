#!/bin/bash

# This script guides a user through setting up the Sphero RVR Python SDK.

# Install the SDK dependencies (only for the current user)
pip3 install --user -r requirements.txt

# Reload ~/.profile.  In recent Raspberry Pi OS releases, this automatically includes $HOME/.local/bin in the path once it exists.
source ~/.profile

# Provide an opportunity to correct the UART settings if needed.
./tools/pi-uart-check.sh
