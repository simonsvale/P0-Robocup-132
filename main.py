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

global calibrated_grey_line, calibrated_white_line, threshold, section_number, flask_constant, number

kontroller = EV3Brick()                          # Main LEGO brick

motorGrip = Motor(Port.C, Direction.CLOCKWISE)    # Assigning the small motor to a variable.

motorR = Motor(Port.A, Direction.CLOCKWISE)       # Assigning the motors to variables.
motorL = Motor(Port.D, Direction.CLOCKWISE)

dist_sensor = UltrasonicSensor(Port.S3)           # Assigning the distance (Ultrasonic sensor) sensor to a variable.
line_sensor = ColorSensor(Port.S4)               # Assigning the colour sensor to a variable.

calibration_drive = DriveBase(right_motor = motorR, left_motor = motorL, wheel_diameter=68.8, axle_track=135)  

drive_speed = 230                             # Used power of motor in % ?        

# 0 = beginning
section_number = 0

threshold = 0

number = 0


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
     wait(1200)
     calibration_drive.stop()
     calibrated_white_line = line_sensor.reflection()
     kontroller.screen.draw_text(1, 20, line_sensor.reflection()) # debug
     
     # Drive backwards and turn again.
     wait(100)
     calibration_drive.drive(-100, 0)
     wait(1200)
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
     global section_number, threshold, flask_constant
     
     flask_constant = 1
     
     if section_number == 3 and number < 1000:
          flask_constant = 2.5
          
     if section_number == 12:
          flask_constant = 2

     difference = threshold - line_sensor.reflection() 
     turn_rate = flask_constant*0.0048*(difference)**3
     
     if line_sensor.reflection() > 80:
          calibration_drive.drive(drive_speed, turn_rate)

     if 80 >= line_sensor.reflection() > 69:
          calibration_drive.drive(drive_speed, turn_rate)
     
     if 69 >= line_sensor.reflection() > 60:
          calibration_drive.drive(drive_speed, turn_rate)    
          
     # Blackline stop
     if  3 < line_sensor.reflection() < 11:
          calibration_drive.stop()
          section_number += 1
          kontroller.speaker.beep() #Debug 

def section_1():
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-190, 20)
     wait(500)
     calibration_drive.stop()
     wait(50)
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while 90 < line_sensor.reflection() <= 100:
          calibration_drive.drive(100, 0) 
     
     while line_sensor.reflection() <= 95:
          calibration_drive.drive(100, 0)

     wait(650)
     calibration_drive.stop()
     
     # Turn again.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(95, 18)
     wait(750)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while section_number == 1:
          line_follow()

def section_2():
     global drive_speed, number
     # Drive a bit forward.
     calibration_drive.drive(200, 0)
     wait(400)
     calibration_drive.stop()
     
      # Turn the robot.
     motorR = Motor(Port.A, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-95, 18)
     wait(750)
     calibration_drive.stop()
     motorR = Motor(Port.A, Direction.CLOCKWISE)
          
     while 90 < line_sensor.reflection() <= 100:
          calibration_drive.drive(100, 0)
     
     calibration_drive.stop()
     drive_speed = 95
     
     calibration_drive.drive(100, 0)
     wait(500)
     
     
     # Turn again.
     calibration_drive.stop()
     motorR = Motor(Port.A, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(95, 18)
     wait(700)
     calibration_drive.stop()
     motorR = Motor(Port.A, Direction.CLOCKWISE)

     
     while section_number == 2:
          line_follow()
          number += 1
          if number > 1200:
               drive_speed = 230
     
     number = 0

def section_3():
     global drive_speed, flask_constant, section_number, number
     if number <= 150:
          drive_speed = 50
     line_follow()
     if number > 1000:
          drive_speed = 120
     number += 1
          
     if dist_sensor.distance() < 100:
          calibration_drive.stop()
          wait(1)
          calibration_drive.drive(50, 0)
          wait(400)
          motorGrip.run(-300)
          wait(2200)
          motorGrip.stop() 
          
          while line_sensor.reflection() > 10:
               calibration_drive.drive(100, 0)
          
          wait(100)
          calibration_drive.stop()
          motorGrip.run(300)
          wait(2200)
          motorGrip.stop()
          wait(100)
          
          
          section_number += 1
          line_count = 0
          kontroller.speaker.beep() #Debug 

def section_4():
     global drive_speed
     calibration_drive.drive(-250, 0)
     wait(2470)
     calibration_drive.drive(50, -40)
     wait(2200)
     calibration_drive.stop()
     while section_number == 4:
          drive_speed = 230
          line_follow()
     
def section_5():
     global drive_speed, flask_constant
     drive_speed = 250
     line_follow()
  
def section_6():
     global drive_speed, number
     drive_speed = 230
     line_count = 0
     calibration_drive.drive(200, 0)
     wait(1000)
     calibration_drive.stop()
     
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(190, 20)
     wait(500)
     calibration_drive.stop()
     
     # Drive foward.
     wait(50)
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     wait(50)
     calibration_drive.drive(100, 0)
     wait(400)
     calibration_drive.stop()
     
     while line_sensor.reflection() > 90:
          calibration_drive.drive(100, 0)
     wait(300)
     calibration_drive.stop()
          
     while line_sensor.reflection() < 90:
          calibration_drive.drive(100, 0)
     wait(300)
     calibration_drive.stop()
          
     while line_sensor.reflection() > 90:
          calibration_drive.drive(100, 0)
     
     wait(400)
     calibration_drive.stop()
     wait(50)
     
     # Turn again.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-190, 20)
     wait(500)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while section_number == 6:
          line_follow()
     
     # Set number to 0, to prepare for section 7, where we resuse the numbers.
     number = 0
     line_count = 0

def section_7():
     global drive_speed, flask_constant, section_number
     # Turn the robot.
     calibration_drive.drive(100, 0)
     wait(1700)
     calibration_drive.stop()
     
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(100, 20)
     wait(1000)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     calibration_drive.drive(100, 0)
     wait(400)
     calibration_drive.stop()
     
     drive_speed = 80
     
     while section_number == 7:
          line_follow()
     
def section_8():
     global section_number
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(60, 10)
     wait(60)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     line_count = 0
     calibration_drive.drive(60, 0)
     wait(2400)
     calibration_drive.stop()
     while line_count < 3:
          calibration_drive.drive(60, 0)
          if line_sensor.reflection() < 95:
               line_count += 1
               kontroller.speaker.beep()
     
     line_count = 0
     calibration_drive.drive(60, 0)
     wait(300)
     calibration_drive.stop()
     
     # Turn towards the flask.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(50, 8)
     wait(700)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     # Drive forward until flask is seen.
     
     while dist_sensor.distance() > 60:
          calibration_drive.drive(60, 0)
     
     calibration_drive.stop()
     wait(1)
     calibration_drive.drive(60, 0)
     wait(450)
     calibration_drive.stop()
     motorGrip.run(-400)
     wait(2600)
     motorGrip.stop() 
     
     calibration_drive.drive(-70, 0)
     wait(2150)
     calibration_drive.stop()
     
     # Drive backwards until inner ring.
     while line_count < 4:
          calibration_drive.drive(-65, 0)
          if line_sensor.reflection() < 95:
               line_count += 1
               kontroller.speaker.beep()
     
     calibration_drive.stop()
     calibration_drive.drive(60, 0)
     wait(300)
     calibration_drive.stop()
     
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-50, 8)
     wait(500)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     wait(300)
     
     # Open flask grapper.
     motorGrip.run(400)
     wait(2600)
     motorGrip.stop()
     section_number += 1

def section_9():
     global drive_speed
     calibration_drive.drive(-120, 0)
     wait(3000)
     calibration_drive.stop()
     
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-60, 18)
     wait(400)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while line_sensor.reflection() > 90:
          calibration_drive.drive(-200, 0)
     
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-60, 18)
     wait(1600)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while section_number == 9:
          line_follow()
          
     drive_speed = 230
     
def section_10():
     global drive_speed, number
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-50, 20)
     wait(800)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     calibration_drive.drive(50, 0)
     wait(600)
     calibration_drive.stop()
     
     while line_sensor.reflection() > 90:
          calibration_drive.drive(200, 0)
          
     wait(400)
     calibration_drive.stop()
     
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-50, 20)
     wait(2000)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while section_number == 10:
          line_follow()
          
     number = 0
     
def section_11():
     global section_number, drive_speed
     while dist_sensor.distance() > 105:
          calibration_drive.drive(100, 0)
     calibration_drive.stop()
     
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(50, 20)
     wait(1240)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while dist_sensor.distance() > 115:
          calibration_drive.drive(100, 0)
     calibration_drive.stop()
     
     # Turn the robot.
     motorR = Motor(Port.A, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(50, 20)
     wait(2000)
     calibration_drive.stop()
     motorR = Motor(Port.A, Direction.CLOCKWISE)
     
     calibration_drive.drive(100, 0)
     wait(2800)
     calibration_drive.stop()
     
      # Turn the robot.
     motorR = Motor(Port.A, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-50, 20)
     wait(1000)
     calibration_drive.stop()
     motorR = Motor(Port.A, Direction.CLOCKWISE)
     
     calibration_drive.drive(150, 0)
     wait(1800)
     calibration_drive.stop()
     
     drive_speed = 150
     while section_number == 11:
          line_follow()
          
     drive_speed = 230

def section_12():
     global drive_speed
     # Turn the robot.
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(-50, 20)
     wait(800)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     calibration_drive.drive(170, 0)
     wait(3570)
     calibration_drive.stop()
     
     motorL = Motor(Port.D, Direction.COUNTERCLOCKWISE)
     calibration_drive.drive(80, 20)
     wait(1200)
     calibration_drive.stop()
     motorL = Motor(Port.D, Direction.CLOCKWISE)
     
     while line_sensor.reflection() > 90:
          calibration_drive.drive(170, 0)
     calibration_drive.stop()
     
     drive_speed = 90
     while section_number == 12:
          line_follow()
     
def section_13():
     global drive_speed, number
     calibration_drive.drive(50, 0)
     wait(900)
     calibration_drive.stop()
     
     drive_speed = 80
     
     while number < 300:
          number += 1
          line_follow()
     
     calibration_drive.stop()
     
     calibration_drive.drive(700, 0)
     wait(3770)
     calibration_drive.stop()
     kontroller.speaker.say("I'm fast as fock Boi!")
     section_number += 1

# The course
def forever():
     global section_number, threshold
     
     while section_number <= 13:
          if section_number == 0:
               calibrate()
               while section_number == 0:
                    line_follow()
          
          if section_number == 1:
               section_1()
               
          if section_number == 2:
               section_2()
          
          if section_number == 3:
               section_3()
               
          if section_number == 4:
               section_4()
               
          if section_number == 5:
               section_5()
          
          if section_number == 6:
               section_6()
          
          if section_number == 7:
               section_7()
          
          if section_number == 8:
               section_8()
               
          if section_number == 9:
               section_9()
          
          if section_number == 10:
               section_10()
               
          if section_number == 11:
               section_11()
          
          if section_number == 12:
               section_12()
               
          if section_number == 13:
               section_13()

forever()