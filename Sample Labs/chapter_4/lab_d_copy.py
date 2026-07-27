"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab_d.py

Title: Lab D - Driving in Mazes

Author: Tianyi Ruan

Purpose: Create a script to enable semi-autonomous driving for the RACECAR. Button presses
enable a series of instructions sent to the RACECAR, which enable it to drive in various shapes.
Complete the lines of code under the #TODO indicators to complete the lab.

Expected Outcome: When the user runs the script, they are able to control the RACECAR
using the following keys:
- When the "A" button is pressed, drive through the obstacle "Zigzag"
- When the "B" button is pressed, drive through the obstacle "Spiral"
- When the "X" button is pressed, drive through the obstacle "Hallway"
- When the "Y" button is pressed, drive through the obstacle "Maze"
"""

########################################################################################
# Imports
########################################################################################

import sys
import time

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# A queue of driving steps to execute
# Each entry is a list containing (time remaining, speed, angle)
queue = []
speed = 0
angle = 0
time_start = 0

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    # Begin at a full stop
    rc.drive.stop()

    # Begin with an empty queue
    queue.clear()

    # Print start message
    print(
        ">> Lab D - Driving in Mazes\n"
        "\n"
        "Controls:\n"
        "   A button = drive through obstacle: \"Zigzag\"\n"
        "   B button = drive through obstacle: \"Spiral\"\n"
        "   X button = drive through obstacle: \"Hallway\"\n"
        "   Y button = drive through obstacle: \"Maze\"\n"
    )


# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global queue
    global speed
    global angle
    global time_start

    current_time = time.perf_counter()

    time_now = current_time - time_start
    while len(queue) > 0 and queue[0][0] <= time_now:
        queue.pop(0)

    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]

        # Deal with what happens when the RACECAR gets too close to a wall
        # 1. Fetch the latest LIDAR scan
        # This returns an array of distance measurements in cm.
        # scan = rc.lidar.get_samples()

        # # 2. Define the window angle (e.g., average over a 5-degree spread)
        # WINDOW_ANGLE = 5

        # # 3. Calculate the distance in each cardinal direction
        # front_dist = rc_utils.get_lidar_average_distance(scan, 0, WINDOW_ANGLE)
        # right_dist = rc_utils.get_lidar_average_distance(scan, 90, WINDOW_ANGLE)
        # back_dist  = rc_utils.get_lidar_average_distance(scan, 180, WINDOW_ANGLE)
        # left_dist  = rc_utils.get_lidar_average_distance(scan, 270, WINDOW_ANGLE)

        # print(f"Front: {front_dist:.2f}")
        # print(f"Right: {right_dist:.2f}")
        # print(f"Back:  {back_dist:.2f}")
        # print(f"Left:  {left_dist:.2f}")


        # if front_dist < 20:
        #     speed = -0.5
        # elif right_dist < 10:
        #     angle = 0
        # elif back_dist < 10:
        #     speed = 0.5
        # elif left_dist < 10:
        #     angle = 0

        # Send speed and angle commands to the RACECAR
        rc.drive.set_speed_angle(speed, angle)
    else:
        rc.drive.stop()

    # When the A button is pressed, add instructions to drive through the obstacle "Zigzag"
    if rc.controller.was_pressed(rc.controller.Button.A):
        drive_zigzag(current_time)

    # When the B button is pressed, add instructions to drive through the obstacle "Spiral"
    if rc.controller.was_pressed(rc.controller.Button.B):
        drive_spiral(current_time)

    # When the X button is pressed, add instructions to drive through the obstacle "Hallway"
    if rc.controller.was_pressed(rc.controller.Button.X):
        drive_hallway(current_time)

    # When the Y button is pressed, add instructions to drive through the obstacle "Maze"
    if rc.controller.was_pressed(rc.controller.Button.Y):
        drive_maze(current_time)

    # TODO Part 1: Analyze the following code segment that executes instructions from the queue.
    # Fill in the blanks with the missing variable assignments and indicies according to the
    # behavior described by the comment below.

    # If the queue is not empty, follow the current drive instruction

# [FUNCTION] When the function is called, clear the queue, then place instructions
# inside of the queue that cause the RACECAR to drive in the zigzag
def drive_zigzag(current_time):
    global queue
    global time_start

    queue.clear()

    queue.append([1, 0, 0])
    queue.append([3.8, 1, 0])
    queue.append([5.1, 1, 1])
    queue.append([5.6, 1, 0])
    queue.append([6.8, 1, -1])
    queue.append([7.4, 1, 0])
    queue.append([8.4, 0, 0])

    time_start = current_time

    # TODO Part 2: Append the correct variables in the correct order in order
    # for the RACECAR to drive in the "Zigzag" obstacle course
    # [Hint] queue.append([time, speed, angle])


# [FUNCTION] When the function is called, clear the queue, then place instructions
# inside of the queue that cause the RACECAR to drive in the spiral
def drive_spiral(current_time):
    global queue
    global speed
    global angle
    global time_start
    # Use this section to define and tune static variables

    queue.clear()

    queue.append([1, 0, 0])
    queue.append([4.8, 1, 0])
    queue.append([6.0, 1, 1])
    queue.append([9.6, 1, 0])
    queue.append([10.88, 1, 1])
    queue.append([13.48, 1, 0])
    queue.append([14.68, 1, 1])
    queue.append([16.28, 1, 0])
    queue.append([17.48, 1, 1])
    queue.append([17.88, 1, 0])
    queue.append([18.88, 0, 0])
    time_start = current_time

    # TODO Part 3: Append the instructions into the queue that represent the RACECAR
    # driving in the "Spiral" obstacle course


# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive through the hallway
def drive_hallway(current_time):
    global queue
    global time_start

    # TODO Part 4: Create constants that represent the RACECAR driving through
    # the "Hallway" obstacle course, and then append the instructions in the
    # correct order into the queue for execution

    queue.clear()

    queue.append([2.02, 0, 0])
    queue.append([3.86, 0.5, 0])
    queue.append([4.26, 0.5, 1])
    queue.append([5.59, 0.5, 0])
    queue.append([5.72, 0.5, -1])
    queue.append([6.43, 0.5, 0])
    queue.append([6.57, 0.5, -1])
    queue.append([6.75, 0.5, 0])
    queue.append([7.56, 0.5, -1])
    queue.append([8.34, 0.5, 0])
    queue.append([8.48, 0.5, 1])
    queue.append([8.95, 0.5, 0])
    queue.append([9.14, 0.5, 1])
    queue.append([9.44, 0.5, 0])
    queue.append([9.63, 0.5, 1])
    queue.append([9.80, 0.5, 0])
    queue.append([11.00, 0.5, 1])
    queue.append([11.36, 0.5, 0])
    queue.append([11.57, 0.5, -1])
    queue.append([12.13, 0.5, 0])
    queue.append([12.67, 0.5, -0.8])
    queue.append([13.17, 0.5, 0])
    queue.append([14.30, 0.5, -1])
    queue.append([14.90, 0.5, 0])
    queue.append([15.12, 0.5, 1])
    queue.append([15.38, 0.5, 0])
    queue.append([15.56, 0.5, 1])
    queue.append([15.78, 0.5, 0])
    queue.append([17.28, 0.5, 1])
    queue.append([18.01, 0.5, 0])
    queue.append([18.54, 0.5, -1])
    queue.append([18.68, 0.5, 0])
    queue.append([19.55, 0.5, -1])
    queue.append([20.04, 0.5, 0])
    queue.append([20.25, 0.5, 1])
    queue.append([21.31, 0.5, 0])
    queue.append([21.43, 0.5, 1])
    queue.append([22.15, 0.5, 0])
    queue.append([24.55, 0, 0])
    queue.append([24.98, 0.5, 0])
    queue.append([25.53, 0, 0])
    queue.append([25.79, 0.5, 0])
    queue.append([26.19, 0, 0])
    queue.append([26.66, 0.5, 0])
    time_start = current_time


# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive in the maze
def drive_maze(current_time):
    global queue
    global speed    
    global angle
    global time_start

    # TODO Part 5: Create constants that represent the RACECAR driving through
    # different parts of the maze, and then append the instructions in the
    # correct order into the queue for execution

    queue.clear()

    queue.append([1.27, 0, 0])
    queue.append([1.35, 0, 1])
    queue.append([1.94, 0, 0])
    queue.append([2.07, 1, 0])
    queue.append([2.16, 0, 0])
    queue.append([7.97, 1, 0])
    queue.append([9.07, 1, -1])
    queue.append([10.05, 1, 0])
    queue.append([10.19, 1, -1])
    queue.append([11.32, 1, 0])
    queue.append([11.78, 0, 0])
    queue.append([12.01, 1, 0])
    queue.append([12.28, 0, 0])
    queue.append([13.15, 0, -1])
    queue.append([13.19, 0, 0])
    queue.append([14.01, -1, 0])
    queue.append([14.10, 0, 0])
    queue.append([14.95, 1, 0])
    queue.append([16.12, 1, -1])
    queue.append([16.15, 0, 0])
    queue.append([18.03, -1, 0])
    queue.append([18.07, 0, 0])
    queue.append([19.32, 1, 0])
    queue.append([21.55, 1, -1])
    queue.append([22.05, 1, 0])
    queue.append([22.43, 1, 1])
    queue.append([23.11, 1, 0])
    queue.append([23.70, 1, 1])
    queue.append([23.74, 0, 1])
    queue.append([25.44, -1, 0])
    queue.append([25.78, 0, 0])
    queue.append([26.41, 1, 0])
    queue.append([27.18, 1, 1])
    queue.append([27.21, 1, 0])
    queue.append([28.57, -1, 0])
    queue.append([28.66, 0, 0])
    queue.append([29.26, 1, 0])
    queue.append([30.37, 1, 1])
    queue.append([30.41, 1, 0])
    queue.append([30.61, -1, 0])
    queue.append([31.74, -1, -1])
    queue.append([31.78, 0, 0])
    queue.append([32.42, 1, 0])
    queue.append([33.95, 1, 1])
    queue.append([34.59, 1, 0])
    queue.append([36.11, 1, -1])
    queue.append([36.59, 1, 0])
    queue.append([37.88, 1, 1])
    queue.append([37.92, 0, 1])
    queue.append([39.90, -1, 0])
    queue.append([40.76, 1, 0])
    queue.append([43.26, 1, 1])
    queue.append([43.56, 1, 0])
    queue.append([44.99, 1, -1])
    queue.append([45.03, 0, -1])
    queue.append([46.14, -1, 0])
    queue.append([46.93, -1, 1])
    queue.append([46.97, 0, 0])
    queue.append([47.76, 1, 0])
    queue.append([49.28, 1, -1])
    queue.append([49.97, 1, 0])
    queue.append([50.23, 1, -1])
    queue.append([52.58, 1, 0])
    queue.append([53.75, 0, 0])
    queue.append([54.51, -1, 0])
    queue.append([55.59, 0, 0])
    queue.append([55.95, -1, 0])
    time_start = current_time

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
