'''
QUB Robotics Society Trash Robots Firmware

--- Robot ---

This code receives button states from a controller over UDP, then sends control signals
to a motor driver based on the received states.

'''

from machine import Pin
import network
import socket

################################
# Configuration
################################

# pin definitions
PIN_LED = 2
PIN_LEFT_A  = 4
PIN_LEFT_B  = 15
PIN_RIGHT_A = 23
PIN_RIGHT_B = 22
SLEEP_TIME = 5

# wifi settings
WIFI_SSID     = "QUBRobots"
WIFI_PASS     = "trash_2024"
ROBOT_IP      = "192.168.1.0"
TRASH_PORT    = 42069



################################
# Hardware setup
################################

# pin objects
led = Pin(PIN_LED, Pin.OUT)
right_a = Pin(PIN_RIGHT_A, Pin.OUT)
right_b = Pin(PIN_RIGHT_B, Pin.OUT)
left_a = Pin(PIN_LEFT_A, Pin.OUT)
left_b = Pin(PIN_LEFT_B, Pin.OUT)

# functions to control the motors
def right_backward():
    right_a.off()
    right_b.on()
def right_forward():
    right_a.on()
    right_b.off()
def right_stop():
    right_a.on()
    right_b.on()
def left_forward():
    left_a.off()
    left_b.on()
def left_backward():
    left_a.on()
    left_b.off()
def left_stop():
    left_a.on()
    left_b.on()
def stop_all():
    left_stop()
    right_stop()

# immediately stop the motors
print("Stopping motors")
left_stop()
right_stop()

# turn LED on to indicate loading
led.value(1)

# connect to wifi network
print(f"Connecting to {WIFI_SSID} wifi")

# enable wifi station (client) mode
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# set static IP address
sta_if.ifconfig((ROBOT_IP, "255.255.0.0", "192.168.0.254", "8.8.8.8"))

# connect!
sta_if.connect(WIFI_SSID, WIFI_PASS)

# wait for wifi
while not sta_if.isconnected(): pass

# we should be connected, print the IP
ip_addr = sta_if.ipconfig("addr4")
print(f"Connected to {WIFI_SSID}, IP is {ip_addr[0]}")

# open socket and start listening
robot_ip = socket.getaddrinfo("0.0.0.0", TRASH_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(robot_ip[0][-1])

# all the setup is complete, turn the led off
print("Robot setup!")



################################
# Main Program
################################

# main program loop
while True:

    # wait for data from the socket
    data, addr = sock.recvfrom(4)
    print(f"Got data from {addr}: {data}")

    # parse the socket data into a list of button values
    btns = list(data)

    # control the motor driver depending on which button was pressed
    # (note: only one of these conditions will be executed at a time)
    if btns[0]:
        left_forward()
        right_forward()
    elif btns[1]:
        left_backward()
        right_backward()
    elif btns[2]:
        left_forward()
        right_stop()
    elif btns[3]:
        left_stop()
        right_forward()
    else:
        left_stop()
        right_stop()