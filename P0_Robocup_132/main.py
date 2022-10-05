#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait
from pybricks.robotics import DriveBase

global calibrated_grey_line, calibrated_white_line, threshold, section_number, turn_constant, number

# Main LEGO brick
EV3 = EV3Brick()

# Assigning the small motor to a variable.
motor_grip = Motor(Port.C, Direction.CLOCKWISE)

# Assigning the drivemotors to variables.
motor_right = Motor(Port.A, Direction.CLOCKWISE)
motor_left = Motor(Port.D, Direction.CLOCKWISE)

# Assigning the distance (Ultrasonic sensor) sensor to a variable.
dist_sensor = UltrasonicSensor(Port.S3)

# Assigning the colour sensor to a variable.
line_sensor = ColorSensor(Port.S4)

drivetrain = DriveBase(right_motor=motor_right,left_motor=motor_left, wheel_diameter=68.8, axle_track=135)

drive_speed = 230 ; section_number = 0 ; number = 0 ; threshold = 0


def claw(claw_speed, claw_time):
    """Open and close the EV3s claw.

    :claw_speed: At what speed the claw should open(+) or close(-) in degrees pr seconds
    :claw_time: For how long the claw should run in milliseconds (ms)
    """
    motor_grip.run(claw_speed)
    wait(claw_time)
    motor_grip.stop()


def flip_wheel_left_and_turn(drive_speed, dgs, drive_time):
    """Turns the EV3 on spot by re-assigning the left wheel to the counter clockwise direction, 
    and running both motors.

    :drive_speed: The velocity of the wheels in millimetres per second.
    :dgs: How many degrees per seconds the wheels should turn.
    :drive_time: For how long this function
    """
    motor_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(drive_speed, dgs)
    wait(drive_time)
    drivetrain.stop()
    motor_left = Motor(Port.D, Direction.CLOCKWISE)


def flip_wheel_right_and_turn(drive_speed, dgs, drive_time):
    """Turns the EV# op spot by re-assigning the right wheel to the clockwise direction,
    and running both motors.

    :drive_speed: The velocity of the wheels in millimetres per second.
    :dgs: How many degrees per seconds the wheels should turn.
    :drive_time: For how long this function
    """
    motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    drivetrain.drive(drive_speed, dgs)
    wait(drive_time)
    drivetrain.stop()
    motor_right = Motor(Port.A, Direction.CLOCKWISE)


def drive_straight(drive_speed, drive_time, dgs=0):
    """Drives the EV3 in a straight line for drive_time seconds.

    :drive_time: How long it should take to drive straight.
    :drive_speed: The velocity of the wheels in millimetres per second.
    :dgs: How many degrees per seconds the wheels should turn.
    """
    drivetrain.drive(drive_speed, dgs)
    wait(drive_time)
    drivetrain.stop()


def calibrate():
    """Calibrates the EV3 by calculating the threshold between grey and white."""
    global threshold

    # Calibrate grey.
    calibrated_grey_line = line_sensor.reflection()

    # Turn the EV3.
    flip_wheel_left_and_turn(-100, 10, 400)

    # Drive forward, calibrate white and stop.
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
    """Follow the grey line.

    :turn_constant: How much the EV3 should correct. Default is 1. 
    """
    global section_number, threshold
    if section_number == 3 and number > 2000:
        turn_constant = 1

    difference = threshold - line_sensor.reflection()
    turn_rate = turn_constant*0.0048*(difference)**3
    drivetrain.drive(drive_speed, turn_rate)

    # Blackline stop
    if 3 < line_sensor.reflection() < 11:
        drivetrain.stop()
        section_number += 1
        EV3.speaker.beep()


def section_1():
    """Run section 1."""
    
    # Turn the EV3 to the right.
    flip_wheel_left_and_turn(-190, 20, 500)

    # When it meets the grey line, continue...
    while 90 < line_sensor.reflection() <= 100:
        drivetrain.drive(100, 0)

    # over the grey line again. 
    while line_sensor.reflection() <= 95:
        drivetrain.drive(100, 0)
    wait(650)
    drivetrain.stop()

    # Turn the EV3 to the left.
    flip_wheel_left_and_turn(95, 18, 750)

    # When done, follow the line to the next section.
    while section_number == 1:
        line_follow()


def section_2():
    """Run section 2."""
    global drive_speed, number

    # Drive a bit forward.
    drive_straight(200, 400)

    # Turn the EV3 to the left.
    flip_wheel_right_and_turn(-95, 18, 750)

    # Search for the grey line.
    while 90 < line_sensor.reflection() <= 100:
        drivetrain.drive(100, 0)

    drivetrain.stop()
    drive_speed = 95
    drive_straight(100, 500)

    # Turn the EV3 to the right.
    flip_wheel_right_and_turn(95, 18, 700)

    # Follow the line slow, the fast.
    while section_number == 2:
        line_follow()
        if number > 1200:
            drive_speed = 230
        else:
            number += 1

    # Set number to 0, for use in other functions.
    number = 0


def section_3():
    """Run section 3."""
    global drive_speed, section_number, number

    # Drive very slow...
    if number <= 600:
        drive_speed = 50
    number += 1

    # and follow the line very aggressively.
    line_follow(2.5)

    # Then drive a bit faster.
    if 2800 > number > 2400:
        drive_speed = 120
        

    # After some time...
    if number > 2801:
        EV3.speaker.beep()
        drivetrain.stop()
        wait(100)
        motor_right = Motor(Port.A, Direction.COUNTERCLOCKWISE)

        # search for bottle 1
        while dist_sensor.distance() > 200:
            drivetrain.drive(-5, 18)
        drivetrain.stop()
        motor_right = Motor(Port.A, Direction.CLOCKWISE)

        # Drive a little closer to the bottle.
        drivetrain.drive(60, 0)

        # If the bottle has been found, then...
        if dist_sensor.distance() < 199:
            drivetrain.stop()
            drive_straight(50, 1400)

            # Close the claw.
            claw(-200, 2600)

            # And drive over the line.
            while line_sensor.reflection() > 10:
                drivetrain.drive(100, 0)

            wait(100)
            drivetrain.stop()

            # Open the claw.
            claw(200, 2600)

            # Run next section.
            section_number += 1
            number += 1


def section_4():
    """Run section 4."""
    global drive_speed

    # Drive backwards
    drive_straight(-250, 2470)

    # Then turn the EV3, about 90 degrees
    drive_straight(50, 2200, -40)

    # Follow the line to the next section.
    while section_number == 4:
        drive_speed = 230
        line_follow()


def section_5():
    """Run section 5."""
    global drive_speed

    # Speed through this section fast.
    drive_speed = 250
    line_follow()


def section_6():
    """Run section 6"""
    global drive_speed, number
    drive_speed = 230

    # Drive straight, and the turn the EV3 to the left.
    drive_straight(200, 1000)
    flip_wheel_left_and_turn(190, 20, 500)

    # Drive forward.
    wait(100)
    drive_straight(100, 400)

    # When the first grey line has been detected, then continue.
    while line_sensor.reflection() > 90:
        drivetrain.drive(100, 0)
    wait(300)
    drivetrain.stop()

    # Then the second grey line...
    while line_sensor.reflection() < 90:
        drivetrain.drive(100, 0)
    wait(300)
    drivetrain.stop()

    # And the third grey line..
    while line_sensor.reflection() > 90:
        drivetrain.drive(100, 0)
    wait(400)
    drivetrain.stop()

    # Turn to the right, and follow the line to the next section.
    wait(50)
    flip_wheel_left_and_turn(-190, 20, 500)
    while section_number == 6:
        line_follow()

    # Set number to 0 to use in section 7.
    number = 0


def section_7():
    """Run section 7."""
    global drive_speed, section_number

    # Drive a bit forward, and turn to the left.
    drive_straight(100, 1700)
    flip_wheel_left_and_turn(100, 20, 1000)

    # Drive straight very slowly, and follow the line to the next section.
    drive_straight(100, 400)
    drive_speed = 80
    while section_number == 7:
        line_follow()


def section_8():
    """Run section 8."""
    global section_number
    line_count = 0

    # Correct the EV3 angle, so that it meets the middle of the circle.
    flip_wheel_left_and_turn(70, 50, 90)

    # Drive over the normal line, so that the EV3 can count the slender lines correctly.
    drive_straight(60, 2600)

    # Beep when the EV3 drives over a slender line
    while line_count < 3:
        drivetrain.drive(60, 0)
        if line_sensor.reflection() < 95:
            line_count += 1
            wait(100)
            EV3.speaker.beep()

    # Reset line_count, so that is can count again.
    line_count = 0

    # Drive a bit forward, so that the EV3 is in the middle of the circle.
    drive_straight(60, 550)

    # Turn towards the second bottle.
    flip_wheel_left_and_turn(48, 8, 745)

    # Drive forward until the second bottle has been detected.
    while dist_sensor.distance() > 60:
        drivetrain.drive(60, 0)
    drivetrain.stop()

    # Drive closer to the bottle, so that the claw can reach it.
    drive_straight(60, 450)
    #claw(-400, 3000)
    motor_grip.run_until_stalled(-400,then=Stop.HOLD, duty_limit=60)

    # Drive over the outer line of the circle .
    drive_straight(-70, 2150)

    # Drive backwards until the EV3 meets the inner ring.
    while line_count < 4:
        drivetrain.drive(-65, 0)
        if line_sensor.reflection() < 95:
            line_count += 1
            wait(100)
            EV3.speaker.beep()
    drivetrain.stop()

    # Correct the EV3, so that the bottle is as close as possible, to the center of the circle.
    drive_straight(60, 300)

    # Open the claw.
    claw(400, 3000)

    # The continue to the next section.
    section_number += 1


def section_9():
    """Runs section 9."""
    global drive_speed

    # Drive out of the circle, and close the claw.
    drive_straight(-120, 3000)
    motor_grip.run_until_stalled(-600,then=Stop.HOLD, duty_limit=50)

    # Turn the EV3, so that it can 'hit' the grey line.
    flip_wheel_left_and_turn(-70, 22, 600)

    # Drive backwards until the EV3 hits the grey line.
    while line_sensor.reflection() > 90:
        drivetrain.drive(-170, 0)
    motor_grip.stop()
    drivetrain.stop()

    # Turn the EV3 to the left by about 90 degrees, so that is can follow the line.
    flip_wheel_left_and_turn(-60, 22, 1600)
    while section_number == 9:
        line_follow()
    drive_speed = 230


def section_10():
    """Run section 10."""
    global drive_speed, number

    # Turn the EV3 to the right, so that it dose not hit the bottle.
    flip_wheel_left_and_turn(-50, 20, 800)

    # Drive over the black line, and continue until the EV3 meets the grey line.
    drive_straight(50, 600)
    while line_sensor.reflection() > 90:
        drivetrain.drive(200, 0)
    wait(400)
    drivetrain.stop()

    # Turn/correct the EV3 to right, so that it can follow the line to the next section.
    flip_wheel_left_and_turn(-50, 20, 2000)
    drive_speed = 100
    while section_number == 10:
        line_follow()

    # Reset number to use section 13.
    number = 0


def section_11():
    """Run section 11. Avoid the walls"""
    global section_number, drive_speed

    # Drive straight until it meets the first black wall.
    while dist_sensor.distance() > 110:
        drivetrain.drive(100, 0)
    drivetrain.stop()

    # Turn the EV3 to the left.
    flip_wheel_left_and_turn(50, 20, 1220)

    # Drive straight until the EV3 meets the second black wall.
    while dist_sensor.distance() > 115:
        drivetrain.drive(100, 0)
    drivetrain.stop()

    # Turn the EV3 to the right, and drive straight.
    flip_wheel_right_and_turn(50, 20, 2100)
    drive_straight(100, 2800)

    # Turn/correct and drive the EV3 to lineup to the grey line
    flip_wheel_right_and_turn(-57, 20, 1100)
    drive_straight(150, 1800)
    drive_speed = 100

    # Follow the grey line to the next section.
    while section_number == 11:
        line_follow()
    drive_speed = 230


def section_12():
    """Run section 12."""
    global drive_speed

    # Turn the EV3 to the left and drive forward, so it dose not hit the bottle.
    flip_wheel_left_and_turn(-50, 20, 800)
    drive_straight(170, 3570)

    # Turn to the left and drive straight until it meets the grey line.
    flip_wheel_left_and_turn(90, 20, 1200)
    while line_sensor.reflection() > 90:
        drivetrain.drive(170, 0)
    drivetrain.stop()
    drive_speed = 90
    while section_number == 12:
        line_follow(2)


def section_13():
    """Run section 13. The runway"""
    global drive_speed, number

    # Drive a bit straight, and follow the line for a very small period.
    drive_straight(50, 800)
    drive_speed = 60
    while number < 350:
        number += 1
        line_follow(0.8)
    drivetrain.stop()

    # Drive as fast as possible to the middle of the runway.
    drive_straight(700, 3300)
    claw(400, 3500)
    section_number += 1


def main():
    """Main function to run sections."""
    global section_number

    # A major while loop to loop through the sections.
    while section_number <= 13:
        if section_number == 0:
            calibrate()
            while section_number == 0:
                line_follow()

        elif section_number == 1:
            section_1()

        elif section_number == 2:
            section_2()

        elif section_number == 3:
            section_3()

        elif section_number == 4:
            section_4()

        elif section_number == 5:
            section_5()

        elif section_number == 6:
            section_6()

        elif section_number == 7:
            section_7()

        elif section_number == 8:
            section_8()

        elif section_number == 9:
            section_9()

        elif section_number == 10:
            section_10()

        elif section_number == 11:
            section_11()

        elif section_number == 12:
            section_12()

        elif section_number == 13:
            section_13()


main()
