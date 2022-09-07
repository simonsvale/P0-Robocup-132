#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

kontroller = EV3Brick()

# Assigning the small motor to variable.
motorGrip = Motor(Port.C, Direction.CLOCKWISE)

# Assigning the distance (Ultrasonic sensor) sensor to a variable.
dist_sensor = UltrasonicSensor(Port.S3)

# Assigning the motors to variables.
motorL = Motor(Port.D, Direction.CLOCKWISE)
motorR = Motor(Port.A, Direction.CLOCKWISE)

   
# Assigning the colour sensor to a variable.
linie_sensor = ColorSensor(Port.S4)

# Wheel motors drivebase
robot1 = DriveBase(right_motor = motorL, left_motor = motorR, wheel_diameter=22, axle_track=10)

#Reflection variables calculated 
BLACK = 60
WHITE = 99
threshold = (BLACK + WHITE) / 2

# Used power of motor in % ?
DRIVE_SPEED = 1000

# Turning gain variable, higher variable = more turn
PROPORTIONAL_GAIN = 4


# repeat forever
def forever():
     while True:
          screen_draw_reflection()
          black_line_stop()
          grip_flask()
          line_follow()
     
def line_follow():
     # Calculate the deviation from the threshold.
     deviation = linie_sensor.reflection() - threshold
 
     # Calculate the turn rate.
     turn_rate = PROPORTIONAL_GAIN * deviation

     # Set the drive base speed and turn rate.
     robot1.drive(DRIVE_SPEED, turn_rate)

          
def screen_draw_reflection():
     kontroller.screen.draw_text(1, 1, linie_sensor.reflection()) 
     wait(100) 
     kontroller.screen.clear()
     
def black_line_stop():
     if  8 < linie_sensor.reflection() < 11:
          #robot1.motorR.brake()
          kontroller.speaker.beep()
               
def grip_flask():
     #Script for gripping the flask at a certain distance
     if dist_sensor.distance() < 40:
          #Runs the claw for (speed,time)
          kontroller.speaker.beep()

forever()

          

