BLINDINATOR
===========

The Blindinator v1.0 by Ivan Cooper & Meena Shah (safety coordinator)
- Combines computer vision, servos and a laser in a way that NO ONE SHOULD EVER DO
- Created for San Francisco Science Hack Day 2014

SUMMARY
=======
The system consists of:
- the USBlindinator: a "Digispark" USB microcontroller connected to two servos and a laser
- blindinator.py, a program that uses SimpleCV computer vision library to track the user's eye by webcam and communicate its position to the USBlindinator

CAUTION
=======
I made this device so you don't have to. This is a horrible idea. You should not ever make one of these. If you do make one, you may be risking severe eye injury to yourself and you may be liable for injury to others caused by this device. I am not responsible for your behavior if you disregard these instructions. 

HARDWARE
========
This was created on a Windows PC but could easily be ported to work on Linux or Mac OS X.
The USBlindinator parts include:
* Digispark microcontroller
* Two micro-servos (Tower Pro SG92R)
* One TTL-controlled 5mW red laser
* Wire, tape, etc.

SOFTWARE PREREQUISITES
======================
- USBlindinator sketch: Digispark Arduino 1.04 software
- blindinator.py: SimpleCV / Python 2.7 and PyUSB

BUILD/INSTALL/USE
=================
This is a record of what I did. As noted above you should not do this! If you do, I suggest you use a non-laser LED for demonstration and safety.
- connect two micro-servos and lasers to Digispark (pins 0,1,2 leaving 3,4 available for USB communication)
- glue laser to one servo. glue one servo to other servo. attach to laptop screen. see pictures
- install blindinator sketch on Digispark
- run blindinator.py
- CALIBRATE
--    use the w,a,s,z keys on the keyboard to point the laser at the left/right/top/bottom of the camera area
--    use the 0,1 keys to turn the laser on/off while previewing (JUST KIDDING DON'T DO THIS)
--    use the p key to print the current x,y position to the console
--    use the q key to quit
--    edit blindinator.py and enter correct calibration points at the top of the file
- RUN
--    restart blindinator.py
--    use the t,k key to start/stop tracking
--    use the v,o keys to enable/disable screen preview-while-tracking (may impact performance)
--    use the u,f keys to turn safety (autolaser disable) off/on (JUST KIDDING LEAVE THE SAFETY ON)
