"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab_f.py

Title: Lab F - Line Follower

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: Write a script to enable fully autonomous behavior from the RACECAR. The
RACECAR should automatically identify the color of a line it sees, then drive on the
center of the line throughout the obstacle course. The RACECAR should also identify
color changes, following colors with higher priority than others. Complete the lines 
of code under the #TODO indicators to complete the lab.

Expected Outcome: When the user runs the script, they are able to control the RACECAR
using the following keys:
- When the right trigger is pressed, the RACECAR moves forward at full speed
- When the left trigger is pressed, the RACECAR, moves backwards at full speed
- The angle of the RACECAR should only be controlled by the center of the line contour
- The RACECAR sees the color RED as the highest priority, then GREEN, then BLUE
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np
import random

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 20

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))

# TODO Part 1: Determine the HSV color threshold pairs for GREEN and RED
# Colors, stored as a pair (hsv_min, hsv_max) Hint: Lab E!
BLUE = ((80, 70, 70), (130, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 70, 70), (80, 255, 255))  # The HSV range for the color green
RED1 = ((0, 70, 70), (10, 255, 255))  # The HSV range for the color red
RED2 = ((170, 70, 70), (179, 255, 255))  # The HSV range for the color red (wraps around)

# Color priority: Red >> Green >> Blue
COLOR_PRIORITY = (RED1, RED2, GREEN, BLUE)

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
contour = None # The contour used


########################################################################################
# Functions
########################################################################################

# [FUNCTION} Clamps a value between a minimum and maximum value
def clamp(value: float, min: float, max: float) -> float:
    return min if value < min else max if value > max else value

# [FUNCTION] Remaps a value from an old range to a new range
def remap_range(value: float, old_min: float, old_max: float, new_min: float, new_max: float) -> float:
    old_range = old_max - old_min
    new_range = new_max - new_min
    return new_range * (float(value - old_min) / float(old_range)) + new_min

# [FUNCTION] Establishes bang-bang control with 2 magnitudes
def bang_bang_control():
    global contour_center
    global angle
    if contour_center is not None:
        setpoint = rc.camera.get_width() / 2
        error = setpoint - contour_center[1]

        # Bang Bang controller logic
        if error < -100:
            angle = 1
        elif error <-20:
            angle = -.1
        elif error > 100:
            angle = -1
        elif error > 20:
            angle = -0.1
        else:
            angle = 0

# [FUNCTION] Establishes proportional control
def proportional_control():
    global contour_center
    global speed
    global angle
    global contour

    if contour is None or contour_center is None:
        return

    rectangle = cv.boundingRect(contour)
    x, _, w, _ = rectangle
    right_edge = x + w

    # Check if contour is at the edge of the screen
    if right_edge >= rc.camera.get_width() - 10 and x <= 10:
        angle = 1
        return

    setpoint = rc.camera.get_width() / 2
    error = contour_center[1] - setpoint
    if error > 200 or error < -200:
        speed = 0.8
    else:
        speed = 1
    angle = clamp(remap_range(error, -rc.camera.get_width() / 2, rc.camera.get_width() / 2, -3, 3), -1, 1)



# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center
    global contour_area
    global contour
    global COLOR_PRIORITY
    global angle

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # Crop the image to the floor directly in front of the car
        image = rc_utils.crop(image,CROP_FLOOR[0], CROP_FLOOR[1])

        for i in COLOR_PRIORITY:

            # TODO Part 2: Search for line colors, and update the global variables
            # contour_center and contour_area with the largest contour found

            # Search for all contours in the current color
            contours = rc_utils.find_contours(image, i[0], i[1])

            # Find the largest contour
            contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)

            # If there is a contour in the frame
            if contour is not None:
                # Calculate contour information
                contour_center = rc_utils.get_contour_center(contour)
                contour_area = rc_utils.get_contour_area(contour)
                
                # Draw the contour onto the image
                rc_utils.draw_contour(image, contour)
                rc_utils.draw_circle(image, contour_center)

                proportional_control()

                # Stop searching for contours of other colors
                break

            contours = None
            contour = None
            contour_center = None
            contour_area = 0


        # Display the image to the screen
        rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle

    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Set RACECAR speed to max (4 m/s)
    rc.drive.set_max_speed(0.5)

    # Print start message
    print(
        ">> Lab 2A - Color Image Line Following\n"
        "\n"
        "Controls:\n"
        "   Right trigger = accelerate forward\n"
        "   Left trigger = accelerate backward\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle

    # Search for contours in the current color image
    update_contour()

    # TODO Part 3: Determine the angle that the RACECAR should receive based on the current 
    # position of the center of line contour on the screen. Hint: The RACECAR should drive in
    # a direction that moves the line back to the center of the screen.

    # Choose an angle based on contour_center

    # Use the triggers to control the car's speed
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    if speed == 0:
        speed = rt - lt

    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)

# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # Print a line of ascii text denoting the contour area and x-position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
