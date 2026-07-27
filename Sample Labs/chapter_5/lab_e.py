"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab_e.py

Title: Lab E - Stoplight Challenge

Author: Tianyi Ruan

Purpose: Write a script to enable autonomous behavior from the RACECAR. When
the RACECAR sees a stoplight object (colored cube in the simulator), respond accordingly
by going straight, turning right, turning left, or stopping. Append instructions to the
queue depending on whether the position of the RACECAR relative to the stoplight reaches
a certain threshold, and be able to respond to traffic lights at consecutive intersections. 

Expected Outcome: When the user runs the script, the RACECAR should control itself using
the following constraints:
- When the RACECAR sees a BLUE traffic light, make a right turn at the intersection
- When the RACECAR sees an ORANGE traffic light, make a left turn at the intersection
- When the RACECAR sees a GREEN traffic light, go straight
- When the RACECAR sees a RED traffic light, stop moving,
- When the RACECAR sees any other traffic light colors, stop moving.

Considerations: Since the user is not controlling the RACECAR, be sure to consider the
following scenarios:
- What should the RACECAR do if it sees two traffic lights, one at the current intersection
and the other at the intersection behind it?
- What should be the constraint for adding the instructions to the queue? Traffic light position,
traffic light area, or both?
- How often should the instruction-adding function calls be? Once, twice, or 60 times a second?

Environment: Test your code using the level "Neo Labs > Lab 3: Stoplight Challenge".
By default, the traffic lights should direct you in a counterclockwise circle around the course.
For testing purposes, you may change the color of the traffic light by first left-clicking to 
select and then right clicking on the light to scroll through available colors.
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np
import time

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

first_purple = 0
prev_first_purple = 0
first_yellow = 0
prev_first_yellow = 0
stoplight_color = ""
speed = 0
angle = 0
first_red = 0
prev_first_red = 0
first_blue = 0
prev_first_blue = 0
first_green = 0
prev_first_green = 0
first_orange = 0
prev_first_orange = 0
stoplight_size = 0

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour (Adjust threshold!)
MIN_CONTOUR_AREA = 1000

# TODO Part 1: Determine the HSV color threshold pairs for ORANGE, GREEN, RED, YELLOW, and PURPLE
# Colors, stored as a pair (hsv_min, hsv_max)
BLUE = ((90, 150, 150), (120, 255, 255))  # The HSV range for the color blue
GREEN = ((40, 150, 150), (80, 255, 255))  # The HSV range for the color green
RED1 = ((0, 150, 150), (10, 255, 255))   # Lower red range
RED2 = ((170, 150, 150), (179, 255, 255)) # Upper red range
ORANGE = ((10, 150, 150), (25, 255, 255)) # The HSV range for the color orange
YELLOW = ((25, 150, 150), (40, 255, 255)) # The HSV range for the color yellow
PURPLE = ((130, 150, 150), (160, 255, 255)) # The HSV range for the color purple

colors_list = [BLUE, GREEN, RED1, RED2, ORANGE]

# >> Variables
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour

queue = [[1.0, 1.0, 0.0]] # The queue of instructions
stoplight_color = "" # The current color of the stoplight

########################################################################################
# Functions
########################################################################################

# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center
    global contour_area
    global stoplight_color
    global MIN_CONTOUR_AREA
    global stoplight_size
    global queue

    stoplight_color = None

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        # TODO Part 2: Search for line colors, and update the global variables
        # contour_center and contour_area with the largest contour found

        # Take a frame from the camera stream and store it inside the "image" variable
        image = rc.camera.get_color_image()

        # Crop the image 
        image = rc_utils.crop(image, (100, 0), (rc.camera.get_height(), rc.camera.get_width()))

        # Change color space from BGR to HSV
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        # Veriable to find the largest contour among all colors
        traffic_light = None

        mask = None
        
        all_contours = []

        # Checks for each color in the colors list
        for i in colors_list:
            # Converts into the mask for the current color
            mask = cv.inRange(hsv, i[0], i[1])

            # Find valid contours in the mask
            contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            max_contour = None
            contours_filtered = []
            for contour in contours:
                area = cv.contourArea(contour)
                if area > MIN_CONTOUR_AREA:
                    contours_filtered.append(contour)
                    if max_contour is None or area > cv.contourArea(max_contour):
                        max_contour = contour
            contour_area = cv.contourArea(max_contour) if max_contour is not None and len(max_contour) > 0 else 0
            if contour_area >= stoplight_size:
                if max_contour is not None and len(max_contour) >= 1: 
                    if traffic_light is None or contour_area > cv.contourArea(traffic_light):
                        traffic_light = max_contour
                        if cv.contourArea(traffic_light) >= 9400:
                            if i == BLUE:
                                stoplight_color = "BLUE"
                            elif i == GREEN:
                                stoplight_color = "GREEN"
                            elif i == RED1 or i == RED2:
                                stoplight_color = "RED"
                                rc.drive.set_speed_angle(0, 0)
                            elif i == ORANGE:
                                stoplight_color = "ORANGE"
                            elif i == YELLOW:
                                stoplight_color = "YELLOW"
                            elif i == PURPLE:
                                stoplight_color = "PURPLE"
                            print(f"{stoplight_color} traffic light detected!")
                        elif cv.contourArea(traffic_light) < 4000:
                            contour_center = rc_utils.get_contour_center(traffic_light)
                            print(f"Contour center: {contour_center}, Contour area: {contour_area}")
                            try:
                                if contour_center[0] > 50 and queue[0][2] == 0:
                                    if contour_center[1] < 290:
                                        queue.insert(0, [0.001, 1, -0.2])
                                    elif contour_center[1] > 350:
                                        queue.insert(0, [0.001, 1, 0.2])
                            except:
                                if contour_center[1] < 290:
                                    queue.insert(0, [0.001, 1, -0.2])
                                elif contour_center[1] > 350:
                                    queue.insert(0, [0.001, 1, 0.2])

                else:
                    stoplight_size = contour_area
                
                all_contours += contours_filtered


        # Highlight only the detected traffic light contour
        if traffic_light is not None and isinstance(traffic_light, np.ndarray) and traffic_light.shape[0] >= 3:
            cv.drawContours(image, [traffic_light], -1, (10, 100, 190), 3)
        rc.display.show_color_image(image)
                
            
        # 
        

        """ # This part is currently not in use
        # Draw the center of the largest contour (N/A for multiple object detection)
        contour_center = rc_utils.get_contour_center(traffic_light)

        # TODO Part 3: Repeat the search for all potential traffic light colors,
        # then select the correct color of traffic light detected.

        if cv.inRange(image[contour_center[1]][contour_center[0]], BLUE[0], BLUE[1]):
            stoplight_color = "BLUE"
        elif cv.inRange(image[contour_center[1]][contour_center[0]], GREEN[0], GREEN[1]):
            stoplight_color = "GREEN"
        elif cv.inRange(image[contour_center[1]][contour_center[0]], RED[0], RED[1]):             
            stoplight_color = "RED"
        elif cv.inRange(image[contour_center[1]][contour_center[0]], ORANGE[0], ORANGE[1]):
            stoplight_color = "ORANGE"
        elif cv.inRange(image[contour_center[1]][contour_center[0]], YELLOW[0], YELLOW[1]):
            stoplight_color = "YELLOW"
        elif cv.inRange(image[contour_center[1]][contour_center[0]], PURPLE[0], PURPLE[1]):
            stoplight_color = "PURPLE"
        """
        

        # Display the image to the screen
        # rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():

    global queue
    global speed
    global angle
    queue.append([1000, 1, 0])
    speed = 1
    angle = 0
    # Set initial driving speed and angle
    rc.drive.set_speed_angle(0,0)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message (You may edit this to be more informative!)
    print(
        ">> Lab 3 - Stoplight Challenge\n"
        "\n"
        "Controls:\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global first_purple
    global prev_first_purple
    global first_yellow
    global prev_first_yellow
    if first_purple != prev_first_purple:
        prev_first_purple += 1
    if first_yellow != prev_first_yellow:
        prev_first_yellow += 1
    global queue
    global stoplight_color
    global speed
    global angle
    global first_red
    global prev_first_red
    global first_blue
    global prev_first_blue
    global first_green
    global prev_first_green
    global first_orange
    global prev_first_orange

    update_contour()

    if first_red != prev_first_red:
        prev_first_red += 1
    if first_blue != prev_first_blue:
        prev_first_blue += 1
    if first_green != prev_first_green:
        prev_first_green += 1
    if first_orange != prev_first_orange:
        prev_first_orange += 1

    # TODO Part 2: Complete the conditional tree with the given constraints.
    if stoplight_color == "BLUE" and first_blue == prev_first_blue:
        turnRight()
        stoplight_color = None
        prev_first_blue += 1
        first_blue += 30
    elif stoplight_color == "GREEN" and first_green == prev_first_green:
        goStraight()
        stoplight_color = None
        prev_first_green += 1
        first_green += 35
    elif stoplight_color == "RED" and first_red == prev_first_red:
        rc.drive.set_speed_angle(0, 0)
        stoplight_color = None
        prev_first_red += 1
        first_red += 100
        stopNow()
    elif stoplight_color == "ORANGE" and first_orange == prev_first_orange:
        turnLeft()
        stoplight_color = None
        prev_first_orange += 1
        first_orange += 30
        stoplight_color = None
    elif stoplight_color == "PURPLE" and first_purple == prev_first_purple:
        stopNow()
        stoplight_color = None
        prev_first_purple += 1
        first_purple += 100
    elif stoplight_color == "YELLOW" and first_yellow == prev_first_yellow:
        stopNow()
        stoplight_color = None
        prev_first_yellow += 1
        first_yellow += 100
        stoplight_color = None

    # else:
    #     queue.append([0.1, 1, 0])

    # ... You may need more elif/else statements

    # TODO Part 3: Implement a way to execute instructions from the queue once they have been placed
    # by the traffic light detector logic (Hint: Lab 2)

    # Send speed and angle commands to the RACECAR
    # rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)
    
    # Queue stuff, try not to modify

    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]
        queue[0][0] -= rc.get_delta_time()
        if queue[0][0] <= 0:
            queue.pop(0)
    
    rc.drive.set_speed_angle(speed, angle)

"""    
delta_time = rc.get_delta_time()
try:
    if queue[0][0] <= delta_time:
        queue.pop(0)
    else:
        queue[0][0] -= delta_time
    rc.drive.set_speed_angle(queue[0][1], queue[0][2])
except:
    rc.drive.set_speed_angle(1, 0)
 """

# [FUNCTION] Appends the correct instructions to make a 90 degree right turn to the queue
def turnRight():
    global queue
    queue.clear()
    queue.append([0.1, 1, 0])
    queue.append([1.25, 1, 1])
    queue.append([1000, 1, 0])
    # TODO Part 4: Complete the rest of this function with the instructions to make a right turn

# [FUNCTION] Appends the correct instructions to make a 90 degree left turn to the queue
def turnLeft():
    global queue
    queue.clear()
    queue.append([0.1, 1, 0])
    queue.append([1.25, 1, -1])
    queue.append([1000, 1, 0])
    # TODO Part 5: Complete the rest of this function with the instructions to make a left turn

# [FUNCTION] Appends the correct instructions to go straight through the intersectionto the queue
def goStraight():
    pass
    # TODO Part 6: Complete the rest of this function with the instructions to make a left turn

# [FUNCTION] Clears the queue to stop all actions
def stopNow():
    global queue
    global speed
    global angle
    queue.clear()
    queue.append([2, -1, 0])
    queue.append([3, 0, 0])
    
    

def stopNow2():
    global queue
    queue.clear()

def update_slow():
    pass

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()