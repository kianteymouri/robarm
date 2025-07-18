import pygame
import serial
import time

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Set up serial connection to Arduino
arduino = serial.Serial('/dev/tty.usbmodem1301', 9600)  # Replace with your Arduino port
time.sleep(2)

# Initial angles
angle1 = 90  # Servo 1 (left stick)
angle2 = 90  # Servo 2 (right stick)
angle3 = 90 # Servo 3

# Threshold to detect joystick as "pressed"
threshold = 0.9

while True:
    pygame.event.pump()

    # Read Y-axis of left and right joystick
    left_y = -joystick.get_axis(1)   # Left stick Y-axis (Servo 1)
    right_y = -joystick.get_axis(3)  # Right stick Y-axis (Servo 2)
    #middle_y = -joystick.get_button(5) # right trig

    # Handle Servo 1 (left stick)
    if left_y > threshold:
        angle1 += 10  # Joystick pushed up
    elif left_y < -threshold:
        angle1 -= 10  # Joystick pushed down

    # Handle Servo 2 (right stick)
    if right_y > threshold:
        angle2 += 10  # Joystick pushed up
    elif right_y < -threshold:
        angle2 -= 10  # Joystick pushed down

    # Handle Servo 3
   # B maps to button 5
    if joystick.get_button(1):  # RB
        angle3 += 10

    # X maps to button 4
    if joystick.get_button(2):  # LB
        angle3 -= 10


    # Clamp angles between 0 and 180
    angle1 = max(0, min(180, angle1))
    angle2 = max(0, min(180, angle2))
    angle3 = max(0, min(180, angle3))

    # Send updated angles to Arduino
    arduino.write(f"{angle1},{angle2},{angle3}\n".encode('utf-8'))

    time.sleep(0.05)
