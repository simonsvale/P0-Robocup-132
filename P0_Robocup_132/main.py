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



def turn_left(drive_speed, dgs, wait_time):
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(drive_speed, dgs)
    wait(wait_time)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

def turn_right(drive_speed, dgs, wait_time):
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(drive_speed, dgs)
    wait(wait_time)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)

def straight(drive_speed, wait_time):
    drivetrain.drive(drive_speed, 0)
    wait(wait_time)
    drivetrain.stop()

def calibrate(): 
    # Calibrate
    calibrated_grey_line = line_sensor.reflection()

    # Turn the robot.
    turn_left(-100, 10, 400)

    # Drive forward, calibrate and stop.
    wait(50)   
    straight(100, 1200)

    calibrated_white_line = line_sensor.reflection()
   

    # Drive backwards and turn again.
    wait(100)
    straight(-100, 1200)

    wait(50)

    turn_left(100, -10, 400)

    # Calculate the threshold based on the calibrated values.
    threshold = (calibrated_grey_line + calibrated_white_line) / 2

    return threshold

def line_follow():
    global section_number, turn_constant

    turn_constant = 1

    if section_number == 3 and number < 1000:
        turn_constant = 2.5

    if section_number == 12:
        turn_constant = 2

    if section_number == 13:
        turn_constant = 0.5

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
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-190, 20)
    wait(500)
    drivetrain.stop()
    wait(50)
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while 90 < line_sensor.reflection() <= 100:
        drivetrain.drive(100, 0)

    while line_sensor.reflection() <= 95:
        drivetrain.drive(100, 0)

    wait(650)
    drivetrain.stop()

    # Turn again.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(95, 18)
    wait(750)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while section_number == 1:
        line_follow()


def section_2():
    global drive_speed, number
    # Drive a bit forward.
    drivetrain.drive(200, 0)
    wait(400)
    drivetrain.stop()

    # Turn the robot.
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-95, 18)
    wait(750)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)

    while 90 < line_sensor.reflection() <= 100:
        drivetrain.drive(100, 0)

    drivetrain.stop()
    drive_speed = 95

    drivetrain.drive(100, 0)
    wait(500)

    # Turn again.
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(95, 18)
    wait(700)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)

    while section_number == 2:
        line_follow()
        number += 1
        if number > 1200:
            drive_speed = 230

    number = 0


def section_3():
    global drive_speed, turn_constant, section_number, number
    if number <= 150:
        drive_speed = 50

    line_follow()

    if 1200 > number > 1000:
        drive_speed = 120
    number += 1

    if number > 1201:
        EV3.speaker.beep()
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
            drivetrain.drive(50, 0)
            wait(1400)
            motor_grip.run(-200)
            wait(2600)
            motor_grip.stop()

            while line_sensor.reflection() > 10:
                drivetrain.drive(100, 0)

            wait(100)
            drivetrain.stop()
            motor_grip.run(200)
            wait(2600)
            motor_grip.stop()
            wait(100)

            section_number += 1
            number += 1
            line_count = 0
            EV3.speaker.beep()  # Debug


def section_4():
    global drive_speed
    drivetrain.drive(-250, 0)
    wait(2470)
    drivetrain.drive(50, -40)
    wait(2200)
    drivetrain.stop()
    while section_number == 4:
        drive_speed = 230
        line_follow()


def section_5():
    global drive_speed, turn_constant
    drive_speed = 250
    line_follow()


def section_6():
    global drive_speed, number
    drive_speed = 230
    line_count = 0
    drivetrain.drive(200, 0)
    wait(1000)
    drivetrain.stop()

    # Turn the robot.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(190, 20)
    wait(500)
    drivetrain.stop()

    # Drive foward.
    wait(50)
    motor_left = Motor(Port.D, Direction.CLOCKWISE)
    wait(50)
    drivetrain.drive(100, 0)
    wait(400)
    drivetrain.stop()

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
    wait(50)

    # Turn again.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-190, 20)
    wait(500)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while section_number == 6:
        line_follow()

    # Set number to 0, to prepare for section 7, where we resuse the numbers.
    number = 0
    line_count = 0


def section_7():
    global drive_speed, turn_constant, section_number
    # Turn the robot.
    drivetrain.drive(100, 0)
    wait(1700)
    drivetrain.stop()

    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(100, 20)
    wait(1000)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    drivetrain.drive(100, 0)
    wait(400)
    drivetrain.stop()

    drive_speed = 80

    while section_number == 7:
        line_follow()


def section_8():
    global section_number
    # Turn the robot.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(60, 10)
    wait(60)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    line_count = 0
    drivetrain.drive(60, 0)
    wait(2600)
    drivetrain.stop()
    while line_count < 3:
        drivetrain.drive(60, 0)
        if line_sensor.reflection() < 95:
            line_count += 1
            wait(100)
            EV3.speaker.beep()

    line_count = 0
    drivetrain.drive(60, 0)
    wait(550)
    drivetrain.stop()

    # Turn towards the flask.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(50, 8)
    wait(745)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    # Drive forward until flask is seen.

    while dist_sensor.distance() > 60:
        drivetrain.drive(60, 0)

    drivetrain.stop()
    wait(1)
    drivetrain.drive(60, 0)
    wait(450)
    drivetrain.stop()
    motor_grip.run(-400)
    wait(3000)
    motor_grip.stop()

    drivetrain.drive(-70, 0)
    wait(2150)
    drivetrain.stop()

    # Drive backwards until inner ring.
    while line_count < 4:
        drivetrain.drive(-65, 0)
        if line_sensor.reflection() < 95:
            line_count += 1
            wait(100)
            EV3.speaker.beep()

    drivetrain.stop()
    drivetrain.drive(60, 0)
    wait(300)
    drivetrain.stop()

    # Open flask grapper.
    motor_grip.run(400)
    wait(3000)
    motor_grip.stop()
    section_number += 1


def section_9():
    global drive_speed
    drivetrain.drive(-120, 0)
    wait(3000)
    drivetrain.stop()

    # Close claw.
    motor_grip.run(-270)

    # Turn the robot.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-60, 18)
    wait(500)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while line_sensor.reflection() > 90:
        drivetrain.drive(-200, 0)

    motor_grip.stop()

    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-60, 18)
    wait(1600)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while section_number == 9:
        line_follow()

    drive_speed = 230


def section_10():
    global drive_speed, number
    # Turn the robot.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-50, 20)
    wait(800)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    drivetrain.drive(50, 0)
    wait(600)
    drivetrain.stop()

    while line_sensor.reflection() > 90:
        drivetrain.drive(200, 0)

    wait(400)
    drivetrain.stop()

    # Turn the robot.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-50, 20)
    wait(2000)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

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
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(50, 20)
    wait(1220)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while dist_sensor.distance() > 115:
        drivetrain.drive(100, 0)
    drivetrain.stop()

    # Turn the robot.
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(50, 20)
    wait(2100)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)

    drivetrain.drive(100, 0)
    wait(2800)
    drivetrain.stop()

    # Turn the robot.
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-50, 20)
    wait(1100)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)

    drivetrain.drive(150, 0)
    wait(1800)
    drivetrain.stop()

    drive_speed = 100
    while section_number == 11:
        line_follow()

    drive_speed = 230


def section_12():
    global drive_speed
    # Turn the robot.
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(-50, 20)
    wait(800)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    drivetrain.drive(170, 0)
    wait(3570)
    drivetrain.stop()

    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(80, 20)
    wait(1200)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)

    while line_sensor.reflection() > 90:
        drivetrain.drive(170, 0)
    drivetrain.stop()

    drive_speed = 90
    while section_number == 12:
        line_follow()


def section_13():
    global drive_speed, number
    drivetrain.drive(50, 0)
    wait(800)
    drivetrain.stop()

    drive_speed = 60

    while number < 250:
        number += 1
        line_follow()

    drivetrain.stop()

    drivetrain.drive(700, 0)
    wait(3800)
    drivetrain.stop()
    EV3.speaker.say("I'm fast as fock Boi!")

    motor_grip.run(400)
    wait(3500)
    motor_grip.stop()

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