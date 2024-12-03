'''
QUB Robotics Society Trash Robots Firmware

--- Controller ---

This code continuously reads the state of a list of buttons, then
packages the states into a list, and transmits it to a device on
the same network over UDP.

'''

from machine import Pin
import network
import socket
from time import sleep

################################
# Configuration
################################

# pin definitions
PIN_BTN_UP = 14
PIN_BTN_DOWN = 22
PIN_BTN_LEFT = 23
PIN_BTN_RIGHT = 18
PIN_LED = 2

# wifi settings
WIFI_SSID     = "QUBRobots"
WIFI_PASS     = "trash_2024"
ROBOT_IP      = "192.168.1.0"
CONTROLLER_IP = "192.168.2.0"
TRASH_PORT    = 42069



################################
# Hardware setup
################################

# pin objects
btn_up = Pin(PIN_BTN_UP, Pin.IN, Pin.PULL_DOWN)
btn_down = Pin(PIN_BTN_DOWN, Pin.IN, Pin.PULL_DOWN)
btn_left = Pin(PIN_BTN_LEFT, Pin.IN, Pin.PULL_DOWN)
btn_right = Pin(PIN_BTN_RIGHT, Pin.IN, Pin.PULL_DOWN)
btn_pins = [btn_up, btn_down, btn_left, btn_right]
led = Pin(PIN_LED, Pin.OUT)

# turn LED on to indicate loading
led.value(1)

# connect to wifi network
print(f"Connecting to {WIFI_SSID} wifi")

# enable wifi station (client) mode
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# set static IP address
sta_if.ifconfig((CONTROLLER_IP, "255.255.0.0", "192.168.0.254", "8.8.8.8"))

# connect!
sta_if.connect(WIFI_SSID, WIFI_PASS)

# wait for wifi
while not sta_if.isconnected(): pass

# we should be connected, print the IP
ip_addr = sta_if.ipconfig("addr4")
print(f"Connected to {WIFI_SSID} wifi, IP is {ip_addr[0]}")

# open UDP socket to robot's IP
robot_ip = socket.getaddrinfo(ROBOT_IP, TRASH_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Opening socket to robot at {robot_ip[0][-1][0]}")
sock.connect(robot_ip[0][-1])
print(f"Socket opened")

# all the setup is complete, turn the led off
print("Controller setup!")
led.value(0)



################################
# Main Program
################################

btns      = [0, 0, 0, 0]    # list to store the current state of the buttons
last_btns = [0, 0, 0, 0]    # list to store the button state of the last iteration
changed   = False

# main program loop
# this constantly reads the value of each button pin
while True:

    # read the state of each pin and check if a pin has changed
    for i, btn_pin in enumerate(btn_pins):
        last_btns[i] = btns[i]
        btns[i] = btn_pin.value();
        if btns[i] != last_btns[i]: 
            changed = True
            print(f"btn {i} changed from {last_btns[i]} to {btns[i]}")

    if changed: 

        # convert the current button state to a byte array, and send it over the socket
        sock.sendall(bytes(btns))

        # reset changed variable for next iteration
        changed = False