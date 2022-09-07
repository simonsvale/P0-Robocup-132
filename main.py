#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

kontroller = EV3Brick()

# Assigning the motors to variables.
motorL = Motor(Port.D, Direction.CLOCKWISE)
motorR = Motor(Port.A, Direction.CLOCKWISE)

# Assigning the small motor to variable.
motorGrip = Motor(Port.C, Direction.CLOCKWISE)


# Assigning the colour sensor to a variable.
linie_sensor = ColorSensor(Port.S4)

# Assigning the distance (Ultrasonic sensor) sensor to a variable.
distance_sensor = UltrasonicSensor(Port.S3)

robot1 = DriveBase(right_motor = motorL, left_motor = motorR, wheel_diameter=22, axle_track=10)

# Reflection variables calculated 
BLACK = 60
WHITE = 99
threshold = (BLACK + WHITE) / 2

# Used power of motor in % ?
DRIVE_SPEED = 1000

# Turning gain variable, higher variable = more turn
PROPORTIONAL_GAIN = 4

while True:
    # Calculate the deviation from the threshold.
    deviation = linie_sensor.reflection() - threshold

    kontroller.screen.draw_text(30, 20, linie_sensor.reflection())
    
    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * deviation

    # Set the drive base speed and turn rate.
    robot1.drive(DRIVE_SPEED, turn_rate)

    # stops at black border.
    if  8 < linie_sensor.reflection() < 11:
         robot1.motorR.brake()
         
    wait(10)
    kontroller.screen.clear()

#Script for 
if distance < 3.0:
     robot1.motorGrip


