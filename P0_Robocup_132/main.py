#!/usr/bin/env pybricks-micropython

# 2022 P0 Project
# NAMES HERE ©

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


global calibrated_grey_line, calibrated_white_line, threshold, section_number, turn_constant, number

EV3 = EV3Brick()                          # Main LEGO brick

# Assigning the small motor to a variable.
motor_grip = Motor(Port.C, Direction.CLOCKWISE)

# Assigning the motors to variables.
motor_right = Motor(Port.A, Direction.CLOCKWISE)
motor_left = Motor(Port.D, Direction.CLOCKWISE)

# Assigning the distance (Ultrasonic sensor) sensor to a variable.
dist_sensor = UltrasonicSensor(Port.S3)
# Assigning the colour sensor to a variable.
line_sensor = ColorSensor(Port.S4)

drivetrain = DriveBase(right_motor=motor_right, left_motor=motor_left, wheel_diameter=68.8, axle_track=135)

drive_speed = 230

# 0 = beginning
section_number = 0
number = 0
threshold = 0

def claw(claw_speed, claw_time):
    motor_grip.run(claw_speed)
    wait(claw_time)
    motor_grip.stop()


def flip_wheel_left_and_turn(drive_speed, dgs, drive_time):
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(drive_speed, dgs)
    wait(drive_time)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)


def flip_wheel_right_and_turn(drive_speed, dgs, drive_time):
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(drive_speed, dgs)
    wait(drive_time)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)


def drive_straight(drive_speed, drive_time, dgs=0):
    drivetrain.drive(drive_speed, dgs)
    wait(drive_time)
    drivetrain.stop()


def calibrate(): 
    global threshold
    # Calibrate
    calibrated_grey_line = line_sensor.reflection()

    # Turn the robot.
    flip_wheel_left_and_turn(-100, 10, 400)

    # Drive forward, calibrate and stop.
    wait(50)   
    drive_straight(100, 1200)
    calibrated_white_line = line_sensor.reflection()
   
    # Drive backwards and turn again.
    wait(100)
    drive_straight(-100, 1200)
    wait(50)
    flip_wheel_left_and_turn(100, -10, 400)

    # Calculate the threshold based on the calibrated values.
    threshold = (calibrated_grey_line + calibrated_white_line) / 2


def line_follow(turn_constant=1):
    global section_number, threshold

    if section_number == 3 and number > 1000:
        turn_constant = 1

    difference = threshold - line_sensor.reflection()
    turn_rate = turn_constant*0.0048*(difference)**3

    if line_sensor.reflection() > 80:
        drivetrain.drive(drive_speed, turn_rate)

    if 80 >= line_sensor.reflection() > 69:
        drivetrain.drive(drive_speed, turn_rate)

    if 69 >= line_sensor.reflection() > 60:
        drivetrain.drive(drive_speed, turn_rate)

    # Blackline stop
    if 3 < line_sensor.reflection() < 11:
        drivetrain.stop()
        section_number += 1
        EV3.speaker.beep()  # Debug


def section_1():
    # Turn the robot.
    flip_wheel_left_and_turn(-190, 20, 500)

    while 90 < line_sensor.reflection() <= 100:
        drivetrain.drive(100, 0)

    while line_sensor.reflection() <= 95:
        drivetrain.drive(100, 0)

    wait(650)
    drivetrain.stop()

    flip_wheel_left_and_turn(95, 18, 750)

    while section_number == 1:
        line_follow()


def section_2():
    global drive_speed, number
    # Drive a bit forward.
    drive_straight(200, 400)

    # Turn the robot.
    flip_wheel_right_and_turn(-95, 18, 750)

    while 90 < line_sensor.reflection() <= 100:
        drivetrain.drive(100, 0)

    drivetrain.stop()
    drive_speed = 95
    drive_straight(100, 500)
    
    # Turn again
    flip_wheel_right_and_turn(95, 18, 700)

    while section_number == 2:
        line_follow()
        if number > 1200:
            drive_speed = 230
        else:
            number += 1
    number = 0


def section_3():
    global drive_speed, section_number, number

    if number <= 150:
        drive_speed = 50

    line_follow(2.5)

    if 1400 > number > 1000:
        drive_speed = 120

    if number > 1401:
        drivetrain.stop()
        wait(100)
        motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)

        while dist_sensor.distance() > 200:
            drivetrain.drive(-5, 18)

        drivetrain.stop()
        motor_right = Motor(Port.A, Direction.CLOCKWISE)

        drivetrain.drive(60, 0)

        if dist_sensor.distance() < 199:
            drivetrain.stop()
            drive_straight(50, 1400)

            claw(-200, 2600)

            while line_sensor.reflection() > 10:
                drivetrain.drive(100, 0)

            wait(100)
            drivetrain.stop()

            claw(200, 2600)

            section_number += 1
            number += 1

    number += 1


def section_4():
    global drive_speed
    drive_straight(-250, 2470)

    drive_straight(50,2200, -40)

    while section_number == 4:
        drive_speed = 230
        line_follow()


def section_5():
    global drive_speed
    drive_speed = 250
    line_follow()


def section_6():
    global drive_speed, number
    drive_speed = 230

    drive_straight(200, 1000)

    # Turn the robot.
    flip_wheel_left_and_turn(190, 20, 500)
 
    # Drive foward.
    wait(100)
    drive_straight(100, 400)

    while line_sensor.reflection() > 90:
        drivetrain.drive(100, 0)
    wait(300)
    drivetrain.stop()

    while line_sensor.reflection() < 90:
        drivetrain.drive(100, 0)
    wait(300)
    drivetrain.stop()

    while line_sensor.reflection() > 90:
        drivetrain.drive(100, 0)

    wait(400)
    drivetrain.stop()

    # Turn again
    wait(50)
    flip_wheel_left_and_turn(-190, 20, 500)

    while section_number == 6:
        line_follow()

    # Set number to 0, to prepare for section 7, where we resuse the numbers.
    number = 0


def section_7():
    global drive_speed, section_number

    # Turn the robot.
    drive_straight(100, 1700)

    flip_wheel_left_and_turn(100, 20, 1000)

    drive_straight(100, 400)

    drive_speed = 80

    while section_number == 7:
        line_follow()


def section_8():
    global section_number

    line_count = 0

    # Turn the robot.
    flip_wheel_left_and_turn(60, 10, 60)

    drive_straight(60, 2600)

    while line_count < 3:
        drivetrain.drive(60, 0)
        if line_sensor.reflection() < 95:
            line_count += 1
            wait(100)
            EV3.speaker.beep()

    line_count = 0
    
    drive_straight(60, 550)

    # Turn towards the flask.
    flip_wheel_left_and_turn(50, 8, 745)

    # Drive forward until flask is seen.
    while dist_sensor.distance() > 60:
        drivetrain.drive(60, 0)

    drivetrain.stop()

    drive_straight(60, 450)
    
    claw(-400, 3000)

    drive_straight(-70, 2150)

    # Drive backwards until inner ring.
    while line_count < 4:
        drivetrain.drive(-65, 0)
        if line_sensor.reflection() < 95:
            line_count += 1
            wait(100)
            EV3.speaker.beep()

    drivetrain.stop()

    drive_straight(60, 300)

    # Open flask grapper.
    claw(400, 3000)

    section_number += 1


def section_9():
    global drive_speed

    drive_straight(-120, 3000)

    # Close claw.
    motor_grip.run(-270)

    # Turn the robot.
    flip_wheel_left_and_turn(-60, 22, 600)

    while line_sensor.reflection() > 90:
        drivetrain.drive(-200, 0)

    motor_grip.stop()
    drivetrain.stop()

    flip_wheel_left_and_turn(-60, 22, 1600)

    while section_number == 9:
        line_follow()

    drive_speed = 230


def section_10():
    global drive_speed, number

    # Turn the robot.
    flip_wheel_left_and_turn(-50, 20, 800)

    drive_straight(50, 600)

    while line_sensor.reflection() > 90:
        drivetrain.drive(200, 0)

    wait(400)
    drivetrain.stop()

    # Turn the robot.
    flip_wheel_left_and_turn(-50, 20, 2000)

    drive_speed = 100
    while section_number == 10:
        line_follow()

    number = 0


def section_11():
    global section_number, drive_speed

    while dist_sensor.distance() > 110:
        drivetrain.drive(100, 0)
    drivetrain.stop()

    # Turn the robot.
    flip_wheel_left_and_turn(50, 20, 1220)

    while dist_sensor.distance() > 115:
        drivetrain.drive(100, 0)
    drivetrain.stop()

    # Turn the robot.
    flip_wheel_right_and_turn(50, 20, 2100)

    drive_straight(100, 2800)

    # Turn the robot.
    flip_wheel_right_and_turn(-50, 20, 1100)

    drive_straight(150, 1800)

    drive_speed = 100
    while section_number == 11:
        line_follow()

    drive_speed = 230


def section_12():
    global drive_speed
    # Turn the robot.
    flip_wheel_left_and_turn(-50, 20, 800)

    drive_straight(170, 3570)

    flip_wheel_left_and_turn(80, 20, 1200)
 
    while line_sensor.reflection() > 90:
        drivetrain.drive(170, 0)
    drivetrain.stop()

    drive_speed = 90
    while section_number == 12:
        line_follow(2)


def section_13():
    global drive_speed, number
    drive_straight(50, 800)

    drive_speed = 60

    while number < 250:
        number += 1
        line_follow(0.5)

    drivetrain.stop()

    drive_straight(700, 3800)
    EV3.speaker.say("I'm fast as fock Boi!")

    claw(400, 3500)

    section_number += 1


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