#!/usr/bin/env python3
import rospy
import numpy as np
import cv2 
import time
import math
from std_msgs.msg import Float64, String, Int32MultiArray, Int32
from geometry_msgs.msg import PoseWithCovarianceStamped
_action = []
_status = 0
_move_or_not = 0
_place = ""
_bodycount = 0


def bodycount_callback(bodycount_data):
    global  _bodycount
    _bodycount = bodycount_data.data



def amclpose_callback(msg):
    global _place

    # Scope of Room A
    a_xstart = 19.665
    a_xend = 25
    a_ystart = -33.343 
    a_yend = -28.538
    # Scope of Room B
    # b_xstart = # 2.4
    # b_xend = # -0.217
    # b_ystart = # -4.5 
    # b_yend = # 1.993


    ax = 21.966
    ay = -30.946

    # agv's amcl pose
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    if (x >= a_xstart) and (x <= a_xend):
        if (y >= a_ystart) and (y <= a_yend):
            _place = "A"
        else:
            _place = "none"
    
    # if math.sqrt((x-ax)**2 + (y - ay)**2) <=1.5:
    #     _place = "A"
    # else:
    #     _place = "none" 

    # if (x == ax) and (y == ay):
    #     _place = "A"
    # else:
    #     _place = "none"

def status_callback(status_data):
    global _status
    _status = status_data.data

def move_or_not_callback(move_or_not_data):
    global _move_or_not
    _move_or_not = move_or_not_data.data


def run():
    global _status, _move_or_not, _bodycount, _place
    # action = list(_action)      #transform to list

    status = _status
    move_or_not = _move_or_not
    result = 0
    place = _place
    bodycount = _bodycount

    #result -> disappear LED
    if ((status == 2) or (status == 5)) and (move_or_not == 0) and (bodycount == 6) and (place == "A"):
        result = 1
            
    else:
        result = 0
    print(result)
    return result


def pubout():
    disappear_result = 0   
    # print(final_action)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        disappear_result= run()
        disappear_result_pub.publish(disappear_result)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('agv_disappear', anonymous=True)
    
    #subscriber
    rospy.Subscriber("/agv_status", Int32, status_callback)
    rospy.Subscriber("/agv_move_or_not", Int32, move_or_not_callback)
    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped,amclpose_callback)
    rospy.Subscriber("/socket/recv", Int32, bodycount_callback)
    #publish
    disappear_result_pub = rospy.Publisher('/disappear_result', Int32, queue_size=10)
    
    try:
        pubout()
    except rospy.ROSInterruptException:
        pass

