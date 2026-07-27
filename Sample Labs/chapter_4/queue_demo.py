"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: queue_demo.py

Title: Queue Demo

Author: Tianyi Ruan

Purpose: To demonstrate how to use queues in RACECAR

Expected Outcome: The car should abide by the instructions in the queue.
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

# Declare any global variables here

global queue
global speed
global angle
queue = []
speed = 0
angle = 0

########################################################################################
# Functions
########################################################################################

def drive_circle():
    global queue

    # circle_time = 5.5
    # brake_time = 0.5

    queue.clear()

    queue.append([6, 1, 1])
    queue.append([0.5, -1, 1])

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    pass # Remove 'pass' and write your source code for the start() function here

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global queue
    global speed
    global angle

    if rc.controller.was_pressed(rc.controller.Button.A):
        drive_circle()

    # If the queue is not empty, follow the current drive instructions
    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]
        queue[0][0] -= rc.get_delta_time()
        if queue[0][0] <= 0:
            queue.pop(0)

        print(queue)
    
    else:
        speed = 0
        angle = 0
    
    rc.drive.set_speed_angle(speed, angle)


# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    pass # Remove 'pass and write your source code for the update_slow() function here


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
