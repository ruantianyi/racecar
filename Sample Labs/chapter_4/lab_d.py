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

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, '../../library')
import racecar_core

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# A queue of driving steps to execute
# Each entry is a list containing (time remaining, speed, angle)
queue = []
speed = 0
angle = 0

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

    # When the A button is pressed, add instructions to drive through the obstacle "Zigzag"
    if rc.controller.was_pressed(rc.controller.Button.A):
        drive_zigzag()

    # When the B button is pressed, add instructions to drive through the obstacle "Spiral"
    if rc.controller.was_pressed(rc.controller.Button.B):
        drive_spiral()

    # When the X button is pressed, add instructions to drive through the obstacle "Hallway"
    if rc.controller.was_pressed(rc.controller.Button.X):
        drive_hallway()

    # When the Y button is pressed, add instructions to drive through the obstacle "Maze"
    if rc.controller.was_pressed(rc.controller.Button.Y):
        drive_maze()

    # TODO Part 1: Analyze the following code segment that executes instructions from the queue.
    # Fill in the blanks with the missing variable assignments and indicies according to the
    # behavior described by the comment below.

    # If the queue is not empty, follow the current drive instruction
    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]
        del_time = rc.get_delta_time()
        queue[0][0] -= del_time
        print(f"Time: {del_time}")
        if queue[0][0] <= 0:
            queue.pop(0)

    # Send speed and angle commands to the RACECAR
    rc.drive.set_speed_angle(speed, angle)


# [FUNCTION] When the function is called, clear the queue, then place instructions
# inside of the queue that cause the RACECAR to drive in the zigzag
def drive_zigzag():
    global queue

    queue.clear()

    queue.append([1, 0, 0])
    queue.append([2.8, 1, 0])
    queue.append([1.3, 1, 1])
    queue.append([0.5, 1, 0])
    queue.append([1.2, 1, -1])
    queue.append([0.6, 1, 0])
    queue.append([1, 0, 0])

    # TODO Part 2: Append the correct variables in the correct order in order
    # for the RACECAR to drive in the "Zigzag" obstacle course
    # [Hint] queue.append([time, speed, angle])


# [FUNCTION] When the function is called, clear the queue, then place instructions
# inside of the queue that cause the RACECAR to drive in the spiral
def drive_spiral():
    global queue
    global speed
    global angle
    # Use this section to define and tune static variables

    queue.clear()

    queue.append([1, 0, 0])
    queue.append([3.8, 1, 0])
    queue.append([1.2, 1, 1])
    queue.append([3.6, 1, 0])
    queue.append([1.28, 1, 1])
    queue.append([2.6, 1, 0])
    queue.append([1.2, 1, 1])
    queue.append([1.6, 1, 0])
    queue.append([1.2, 1, 1])
    queue.append([0.4, 1, 0])
    queue.append([1, 0, 0])

    # TODO Part 3: Append the instructions into the queue that represent the RACECAR
    # driving in the "Spiral" obstacle course


# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive through the hallway
def drive_hallway():
    global queue

    # TODO Part 4: Create constants that represent the RACECAR driving through
    # the "Hallway" obstacle course, and then append the instructions in the
    # correct order into the queue for execution

    queue.clear()

    queue.append([1, 0, 0])
    queue.append([1.65, 1, 0])
    queue.append([0.7, 1, 0.41])

    
    queue.append([1.2, 1, -0.6])
    queue.append([1.3, 1, 0.55])
    queue.append([0.47, 1, 0])
    queue.append([0.1, 1, -0.56])

    queue.append([1.1, 1, -0.6])
    queue.append([1.2, 1, 0.9])
    queue.append([0, 1, 0])
    queue.append([1, 1, -0.8])
    queue.append([1, 1, 0.15])
    queue.append([0.6, -1, 0])
    queue.append([1, 0, 0])


# [FUNCTION] When the function is called, clear the queue, then place instructions 
# inside of the queue that cause the RACECAR to drive in the maze
def drive_maze():
    global queue
    global speed
    global angle

    # TODO Part 5: Create constants that represent the RACECAR driving through
    # different parts of the maze, and then append the instructions in the
    # correct order into the queue for execution

    queue.clear()

    queue.append([1, 0, 0])


    queue.append([6, 1, 0])
    queue.append([1.297, 1, -1])
    queue.append([0.379, 1, 0])
    queue.append([0.092, 1, 1])
    queue.append([0.550, 1, 0])
    queue.append([0.160, 1, 1])
    queue.append([0.614, 1, 0])
    queue.append([0.107, 1, -1])
    queue.append([0.606, 1, 0])
    queue.append([0.696, 1, -1])
    queue.append([1.425, -1, 0])
    queue.append([0.600, -1, 1])
    queue.append([0.048, -1, 0])
    queue.append([0.155, 0, 0])
    queue.append([1.658, 1, 0])
    queue.append([0.692, 1, -1])
    queue.append([1.772, -1, 0])
    queue.append([0.042, 0, 0])
    queue.append([0.979, 1, 0])
    queue.append([1.666, 1, -1])
    queue.append([1.696, 1, 0])
    queue.append([0.739, 1, 1])
    queue.append([0.052, 0, 1])
    queue.append([2.193, -1, 0])
    queue.append([0.040, 0, 0])
    queue.append([1.241, 1, 0])
    queue.append([0.674, 1, 1])
    queue.append([0.052, 0, 1])
    queue.append([1.544, -1, 0])
    queue.append([0.041, 0, 0])
    queue.append([0.961, 1, 0])
    queue.append([1.769, 1, 1])
    queue.append([0.793, 1, 0])
    queue.append([1.261, 1, -1])
    queue.append([0.310, 1, 0])
    queue.append([0.093, 1, 1])
    queue.append([0.308, 1, 0])
    queue.append([1.218, 1, 1])
    queue.append([0.053, 0, 1])
    queue.append([2.431, -1, 0])
    queue.append([0.088, 0, 0])
    queue.append([1.438, 1, 0])
    queue.append([1.669, 1, 1])
    queue.append([1.168, 1, 0])
    queue.append([1.187, 1, -1])
    queue.append([0.053, 0, -1])
    queue.append([2.114, -1, 0])
    queue.append([0.041, 0, 0])
    queue.append([0.652, 1, 0])
    queue.append([1.997, 1, -1])
    queue.append([0.231, 1, 0])
    queue.append([0.179, 1, -1])
    queue.append([0.542, 1, 0])
    queue.append([0.102, 1, 1])
    queue.append([0.408, 1, 0])
    queue.append([0.093, 1, -1])
    queue.append([1.374, 1, 0])
    queue.append([0.105, 0, 0])
    queue.append([0.504, -1, 0])
    queue.append([0.649, 0, 0])
    queue.append([0.692, 1, 0])
    queue.append([0.862, 0, 0])
    queue.append([0.307, 1, 0])
    queue.append([1, 0, 0])

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
