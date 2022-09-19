#!/usr/bin/env pybricks-micropython

# 2022 P0 Project
# NAMES HERE ©

import math

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

global calibrated_grey_line, calibrated_white_line, threshold, section_number

kontroller = EV3Brick()                          # Main LEGO brick

motorGrip = Motor(Port.C, Direction.CLOCKWISE)    # Assigning the small motor to a variable.

motorR = Motor(Port.A, Direction.CLOCKWISE)       # Assigning the motors to variables.
motorL = Motor(Port.D, Direction.CLOCKWISE)

dist_sensor = UltrasonicSensor(Port.S3)           # Assigning the distance (Ultrasonic sensor) sensor to a variable.
line_sensor = ColorSensor(Port.S4)               # Assigning the colour sensor to a variable.

calibration_drive = DriveBase(right_motor = motorR, left_motor = motorL, wheel_diameter=68.8, axle_track=135)  

drive_speed = 160                             # Used power of motor in % ?         

section_number = 0


"""
FUNCTIONS
"""

# Calibrates the robot's color sensor, to the grey line, and the white course.
def calibrate():
     global threshold
     
     # Calibrate 
     calibrated_grey_line = line_sensor.reflection()
     kontroller.screen.draw_text(1, 1, line_sensor.reflection()) # debug
     
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-100, 10)
     wait(400)
     calibration_drive.stop()
     
     # Drive forward, calibrate and stop.
     wait(50)
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     calibration_drive.drive(100, 0)
     wait(1000)
     calibration_drive.stop()
     calibrated_white_line = line_sensor.reflection()
     kontroller.screen.draw_text(1, 20, line_sensor.reflection()) # debug
     
     # Drive backwards and turn again.
     wait(100)
     calibration_drive.drive(-100, 0)
     wait(1000)
     calibration_drive.stop()
     wait(50)
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(100, -10)
     wait(400)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     # Calculate the threshold based on the calibrated values.
     threshold = (calibrated_grey_line + calibrated_white_line) / 2
     
     
def line_follow():

     while True:
          difference = threshold - line_sensor.reflection() 
          turn_rate = (0.0044*(difference)**3)*1.3
          
          if line_sensor.reflection() > 80:
               calibration_drive.drive(drive_speed, turn_rate)
          
          if 80 >= line_sensor.reflection() > 69:
               calibration_drive.drive(drive_speed, turn_rate)
           
          if 69 >= line_sensor.reflection() > 60:
               calibration_drive.drive(drive_speed, turn_rate)    
     
     
     """

# A function that makes the robot follow the grey line.
def line_follow():
     global section_number, threshold
     global drive_speed
     global motorL, motorR
     while section_number == 0:
          
          turn_low = threshold * 1.3
          turn_sharp = threshold * 1.7
          # Calculate the deviation from the threshold.
  
          if line_sensor.reflection() > 95:
               calibration_drive.stop()
               wait(1)
               motorR = Motor(Port.D, Direction.CLOCKWISE)
               wait(1)
               calibration_drive.drive(drive_speed, -30)
               wait(150)
               calibration_drive.stop()
               wait(1)
               motorR = Motor(Port.D, Direction.COUNTERCLOCKWISE)

          if 95 >= line_sensor.reflection() > 67:
               calibration_drive.stop()
               wait(1)
               calibration_drive.drive(drive_speed, turn_low)  
               wait(150)
               
          if 67 >= line_sensor.reflection() > 60:
               calibration_drive.stop()
               wait(1)
               motorL = Motor(Port.A, Direction.CLOCKWISE)
               wait(1)
               calibration_drive.drive(drive_speed, 30)
               wait(150)
               calibration_drive.stop()
               wait(1)
               motorL = Motor(Port.A, Direction.COUNTERCLOCKWISE)
          
          # Blackline stop
          if  3 < line_sensor.reflection() < 11:
               wheels_drive.stop
               section_number += 1
               kontroller.screen.draw_text(1, 40, "Section 0 done") 

     """

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

while section_number == 0:
     line_follow()
#END OF FILE