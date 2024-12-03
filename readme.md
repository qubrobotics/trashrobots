# Trash Robots
Firmware for the Trash Robots event at Queen's University Belfast's Robotics Society.

## Overview
The firmware consists of two MicroPython scripts:
- the **controller** takes input from buttons attached to pins, encodes the values as a byte string, and transmits it over UDP to the...
- **robot**, which parses the received byte string as button inputs, then uses the button values to decide how to control a motor driver

This code is provided as a starting point for robots to be built with, so feel free to clone this repo and modify the code as you like!

## Implementation Details
- the two devices communicate with each other over a Wifi network, via their respective static IPs.  if you're modifying the firmware **make sure you have the right IP addresses** in the "Configuration" section of *both* controller and robot firmware
- by default, devices use the following static IP scheme:
  - robots are on `192.168.1.x`
  - controllers are on `192.168.2.x`
  - where `x` is the same for a pair of controller and robot
- the onboard LED (on pin 2) will turn on on boot, and will turn off when the boot process has finished.  this includes connecting to the wifi network