# This shell script will help with auto-starting the python script
# specified below, after the raspberry-pi boots up. Typically, shell
# sessions start in the /home/pi/ directory, so all path changes are
# relative to that location.

cd <your-repo-path-here>
python rc_async_rvr.py <usb-port-here-in-quotes> 96666
#scrot
