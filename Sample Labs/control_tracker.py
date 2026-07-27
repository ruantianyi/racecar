"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: control_tracker.py

Title: Control tracker

Author: Tianyi Ruan

Purpose: To track the controls used to manually drive the RACEAR through a course
and simplify the commands to easily append to the queue.

Expected Outcome: There should be a list of appends that can be directly added to the list.
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(0, '../library')
try:
    import racecar_core
except:
    sys.path.insert(1, '../../library')
    import racecar_core

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
speed = 0
angle = 0
speed_prev = 0
angle_prev = 0
time = 0

# TODO Change the list name so that it matches the list to be appended to:
list_name = "queue"

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    # Initial speed and angle are both 0. The car should not move.
    rc.drive.set_speed_angle(speed, angle)

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global speed
    global angle
    global speed_prev
    global angle_prev
    global time
    
    if rc.controller.is_down(rc.controller.Button.A):
        speed += 1

    if rc.controller.is_down(rc.controller.Button.B):
        speed -= 1

    if rc.controller.is_down(rc.controller.Button.X):
        angle -= 1

    if rc.controller.is_down(rc.controller.Button.Y):
        angle += 1
    
    rc.drive.set_speed_angle(speed, angle)

    # Track the speed and angle and then print if necessary

    if (speed, angle) == (speed_prev, angle_prev):
        time += rc.get_delta_time()
        

    else:
        time += rc.get_delta_time()
        print(f"    {list_name}.append([{time:.2f}, {speed_prev}, {angle_prev}])")
        time = 0

    speed_prev = speed
    angle_prev = angle

    speed = 0
    angle = 0

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
