#!/usr/bin/env pybricks-micropython

# 2022 P0 Project
# NAMES HERE ©



from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

#
# variables 
#

kontroller = EV3Brick()                           # Main LEGO brick

motorGrip = Motor(Port.C, Direction.CLOCKWISE)    # Assigning the small motor to a variable.

motorL = Motor(Port.A, Direction.CLOCKWISE)       # Assigning the motors to variables.
motorR = Motor(Port.D, Direction.CLOCKWISE)

dist_sensor = UltrasonicSensor(Port.S3)           # Assigning the distance (Ultrasonic sensor) sensor to a variable.
line_sensor = ColorSensor(Port.S4)               # Assigning the colour sensor to a variable.

wheels_drive = DriveBase(right_motor = motorR, left_motor = motorL, wheel_diameter=50, axle_track=10)         # Wheel motors drivebase

calibration_drive = DriveBase(right_motor = motorR, left_motor = motorL, wheel_diameter=50, axle_track=10)  

BLACK = 40 #grey
WHITE = 55
threshold = (BLACK + WHITE) / 2                    # Reflection variables calculated 

drive_speed = 180                              # Used power of motor in % ?

turn_gain = 8                                # Turning gain variable, higher variable = more turn

section_number = 0


#
# FUNCTIONS
#

# Calibrates the robot's color sensor, to the grey line, and the white course.
def calibrate():
     # Calibrate 
     calibrated_grey_line = line_sensor.reflection()
     kontroller.screen.draw_text(1, 1, line_sensor.reflection()) # debug
     
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-100, 100)
     wait(400)
     calibration_drive.stop()
     
     # Drive forward, calibrate and stop.
     wait(50)
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     calibration_drive.drive(100, 100)
     wait(1000)
     calibration_drive.stop()
     calibrated_white_line = line_sensor.reflection()
     kontroller.screen.draw_text(1, 20, line_sensor.reflection()) # debug
     
     # Drive backwards and turn again.
     wait(100)
     calibration_drive.drive(-100, 100)
     wait(1000)
     calibration_drive.stop()
     wait(50)
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(100, 100)
     wait(400)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)




def line_follow():
     # Calculate the deviation from the threshold.
     deviation = line_sensor.reflection() - threshold
 
     # Calculate the turn rate.
     turn_rate = turn_gain * deviation

     # Set the drive base speed and turn rate.
     wheels_drive.drive(drive_speed, turn_rate)
     
     #black_line_stop()
     

def black_line_stop():
     global section_number
     if  3 < line_sensor.reflection() < 10:
          wheels_drive.motorR.brake()
          section_number += 1
          print('stopped at a black line on section', section_number)
          
               
def grip_flask():
     #Script for gripping the flask at a certain distance
     if dist_sensor.distance() < 40:
          #Runs the claw for (speed,time)
          kontroller.speaker.beep()




"""
debug
"""

def debug_screen_draw_reflection():
     kontroller.screen.draw_text(1, 1, line_sensor.reflection()) 
     wait(50) 
     kontroller.screen.clear()  


calibrate()
line_follow()
#END OF FILE