from __future__ import print_function
import time
from sr.robot import *

a_th = 2.0 #float: threshold for the control of the orientation

d_th = 0.4 #float: threshold for the control of the linear distance

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
	seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def move_token():
    """
    Function to move the token behind the robot
    """
    R.grab() #the robot grabs the token
    turn(30,2) #the robot moves the token behind itself
    R.release() #the robot releases the token
    turn(-30,2) #the robot goes back to the initial position


def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
    dist (float): distance of the closest silver token (-1 if no silver token is detected)
    rot_y_s (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER: #the token is silver
            dist = token.dist
            rot_y_s = token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y_s


def avoid_golden_token():
    """
    Function to avoid the closest golden token
    """
    dist = 0.85 #the distance between golden token and robot
    for token in R.see():
        if token.dist <= dist and token.info.marker_type is MARKER_TOKEN_GOLD: #the token is gold
            rot_y_g = token.rot_y
            if -60 < rot_y_g < 0: #if the golden token is to the left of the robot, the robot turns right
                print("Oh no! Turn right")
                turn(7.5,1.5)
            elif 0 < rot_y_g < 60: #if the golden token is to the right of the robot, the robot turns left
                print("Oh no! Turn left")
                turn(-7.5,1.5)


while 1:
    drive(90,0.5)
    dist, rot_y_s = find_silver_token()
    avoid_golden_token()
    print(rot_y_s, dist)
    if dist <= d_th: #if the robot is close to the silver token, it moves the token
		print("Found it!")
		move_token()
    if -3*a_th <= rot_y_s <= 3*a_th:
		#if the robot is well aligned with the token, it goes forward
        print("Go ahead")
    elif -90 < rot_y_s < -a_th: #if the silver token is to the left of the robot, the robot turns left
        print("Left")
        turn(-5.5,1.5)
    elif a_th < rot_y_s < 90: #if the silver token is to the right of the robot, the robot turns right
        print("Righ")
        turn(5.5,1.5)
