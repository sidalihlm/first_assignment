from __future__ import print_function

import time
from sr.robot import *


# We create an object of the class robot .
R = Robot()


#### We declare the variables .

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" float: Threshold for the control of the linear distance"""

primel = []

#### FUNCTIONS FOR THE CODE EXECUTION

def drive(speed):
    """
    Function for setting a linear velocity
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed

def turn(speed):
    """
    Function for setting an angular velocity
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
#### The method for finding the further box.
def find_further_box():
    # we create two lists one for the codes and one for the distences of the boxes .
    codel = []
    distl = []
    i = 1
    # we execute the loop.
    while 1:
        pre_markers = R.see()
        # We create a list which contains the codes that are not in primel list.
        markers = [marker for marker in pre_markers if marker.info.code not in primel]
	# If the robot saw the boxes , it does not turn.
        if len(markers)>0:
            turn(0)
            # We store the codes and the distense of the ditected boxes on the two listes.
            for m in markers:
                box_code = m.info.code
                box_distance = m.dist
                codel.append(box_code)
                distl.append(box_distance)
	    # We return the code of the maximum distance box using the index .
            max_dist = max(distl)
            max_dist_index = distl.index(max_dist)
            code = codel[max_dist_index]
            return code
        # If the the robot could not detect any box the robot turns and print program has ended .
        else:
            turn(50)
            time.sleep(0.1)
            i+=1
            if i>40:
                turn(0)
                print('Could not find any more boxes in the filed.')
                print('PROGRAM HAS ENDED')
                exit()
#### defining the box method for,indicating the distance and the angel of the robot.
def box_code(code):
    while 1:
        i = 1
        time.sleep(0.1)
        try:
            markers = R.see()
            for m in markers:
                if m.info.code == code:
                    box_distance = m.dist
                    box_rot = m.rot_y
            return box_distance, box_rot
        except:
            print('Error in box data while looking for box with code: ', code)
            print(R.see())

def go(dist,rot):
    if rot < -a_th:
        turn(-5)
        print('Changing Rot',dist, rot)
    elif rot > a_th:
        turn(5)
        print('Changing Rot',dist, rot)   
    else:
        turn(0)
        drive(50)
        print('Changing dist',dist, rot)

def go_grab(code):
    print('Executing the Grab function.')
    while 1:
        time.sleep(0.05)
        dist, rot = box_code(code)
        go(dist,rot)
        if dist <= d_th:
            drive(0)
            R.grab()
            break

def go_release(main_code, code):
    print('Executing the Release function')
    while 1:
        time.sleep(0.05)
        dist, rot = box_code(main_code)
        go(dist,rot)
        if dist <= 0.7:
            drive(0)
            R.release()
            primel.append(code)
            return 0

def find_main_box(codel):
    turn(50)
    while 1:
        markers = R.see()
        for m in markers:
            if m.info.code in codel:
                turn(0)
                return m.info.code
                

#### The code loop .

i = 1
while 1:
    # We print the number of the executed loop .
    print('Execution #',i,' of loop.')
    i+=1

    try:
        # we call the method find_further_box() .
        code = find_further_box()
    except:
        print('Error in finding further box')
        exit()

    
    if len(primel) == 0:
        primel.append(code)
        continue
    
    # Execution 
    try:
        go_grab(code)
    except:
        print('Error in grab function')
        continue
    
    try:
        main_code = find_main_box(primel)
    except:
        print('Error in find_main function')
        exit()
    
    try:
        go_release(main_code, code)
    except:
        print('Error in release function')
        continue

    for i in range(10):
        time.sleep(0.2)
        drive(-10)
    print(primel)
