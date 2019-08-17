# Bolt RVR Follow

#### This program demonstrates the IR communication capabilities of RVR and Bolt.

Project Materials:
- One RVR with firmware versions:
    - Nordic 5.0.413
    - ST 5.0.421
- One Device with a demo version of EDU app that enables RVR driving.
- One to Four Bolts
- One to Four Devices running the latest release of the EDU app.

#### The RVR Broadcasting Program:
The `rvr_ir_broadcast.py` program will simply initiate IR broadcasting on RVR on channels 0 and 1.\
Best way to drive RVR is through a demo build of the EDU app available through Hockey.\
The app can be found [here.](https://rink.hockeyapp.net/apps/453797ecab6c4b7bab0ecb4d34be337d). You may need to request\
permission to install. It is currently only available on iOS.\  It is also possible to modify the program to add driving\
commands if so desired. 

#### Running Bolt Program:
Load the `bolt_rvr_follow.lab` into the Sphero EDU app and start the program.\
Bolt will start patrolling back and forth with frownie face. When RVR comes within range, it will stop, and switch\
to a happy face, and start following RVR.
