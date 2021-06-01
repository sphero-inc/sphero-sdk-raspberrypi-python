#!/bin/bash

sudo apt-get update -y

sudo apt-get install -y make \
build-essential \
llvm \
libssl-dev \
bzip2 \
zlib1g-dev \
libbz2-dev \
libreadline6 \
libreadline-dev \
libsqlite3-dev \
libncurses5-dev \
libncursesw5-dev \
xz-utils \
tk-dev \
libffi-dev \
liblzma-dev

pip3 install pipenv

# Reload ~/.profile.  In recent Raspberry Pi OS releases, this automatically includes $HOME/.local/bin in the path once it exists.
source ~/.profile

# Test whether pipenv is in the system path now
if ! which pipenv ; then
    # It's not in the path, so we should add it on boot
    printf "\n# Add $HOME/.local/bin to PATH for pipenv.\n# This was automatically added by Sphero RVR SDK first-time-setup.sh\n" >> ~/.profile
    printf "PATH=\"\$HOME/.local/bin:\$PATH\"\n" >> ~/.profile
    
    # Apply the ~/.profile update to this session as well 
    source ~/.profile
fi

python3 -m pipenv --python /usr/bin/python3.7

# The cryptography package is a dependency, but for some reason pipenv can't always install it correctly, so we'll use pip instead.  ¯\_(ツ)_/¯
python3 -m pipenv run pip install cryptography

python3 -m pipenv install

# Provide an opportunity to correct the UART settings if needed.
./pi-uart-check.sh
