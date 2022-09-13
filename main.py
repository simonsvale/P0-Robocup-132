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

motorL = Motor(Port.D, Direction.CLOCKWISE)       # Assigning the motors to variables.
motorR = Motor(Port.A, Direction.CLOCKWISE)

dist_sensor = UltrasonicSensor(Port.S3)           # Assigning the distance (Ultrasonic sensor) sensor to a variable.
linie_sensor = ColorSensor(Port.S4)               # Assigning the colour sensor to a variable.

wheels_drive = DriveBase(right_motor = motorL, left_motor = motorR, wheel_diameter=50, axle_track=10)          # Wheel motors drivebase

BLACK = 41
WHITE = 99
threshold = (BLACK + WHITE) / 2                    # Reflection variables calculated 

drive_speed = 1000                                 # Used power of motor in % ?

turn_gain = 4                                      # Turning gain variable, higher variable = more turn

section_number = 0


#
# FUNCTIONS
#


# repeat forever
def forever(): 
     global section_number 
     
     if section_number == 0:
          section0()

     if section_number == 1:
          section1()
          
     if section_number == 2:
          section2()
          
     if section_number == 3:
          section3()
          kontroller.speaker.say("I completed the course")
     
  

def section0():          # Sections using line_follow will now work if func section0() is called.
     while section_number == 0:
          debug_screen_draw_reflection()
          line_follow()
          black_line_stop()
          
          
     kontroller.speaker.say("section 0 done")
          

def section1():
     # Doing something static 
     while section_number == 1:
          debug_screen_draw_reflection()
          section1_drive()
          black_line_stop()
     
     kontroller.speaker.say("section 1 done")


def section2():
     1+1
     

def section3():
     1+2

def section1_drive():
     print('doing some driving :-)')
     wait(100)
     print('doing some more of that :-)')



def line_follow():
     # Calculate the deviation from the threshold.
     deviation = linie_sensor.reflection() - threshold
 
     # Calculate the turn rate.
     turn_rate = turn_gain * deviation

     # Set the drive base speed and turn rate.
     wheels_drive.drive(drive_speed, turn_rate)

def black_line_stop():
     global section_number
     if  8 < linie_sensor.reflection() < 11:
          #robot1.motorR.brake()
          section_number += 1
          print('stopped at a black line on section', section_number)
          
               
def grip_flask():
     #Script for gripping the flask at a certain distance
     if dist_sensor.distance() < 40:
          #Runs the claw for (speed,time)
          kontroller.speaker.beep()




#
# debug
#

def debug_screen_draw_reflection():
     kontroller.screen.draw_text(1, 1, linie_sensor.reflection()) 
     wait(100) 
     kontroller.screen.clear()  


forever()

#END OF FILE