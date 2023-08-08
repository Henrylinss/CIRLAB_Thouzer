#!/usr/bin/env python3
import rospy
import numpy as np
import cv2 
import time
from std_msgs.msg import Float64, String, Int32MultiArray, Int32

_bodycount = 0
_abnormal = 0
_recognition = []

def abnormal_callback(abnormal_data):
    global _abnormal
    _abnormal = abnormal_data.data

def bodycount_callback(bodycount_data):
    global _bodycount
    _bodycount = bodycount_data.data

def recognition_callback(recognition_data):
    global _recognition


    recognition = recognition_data.data
    recognition_np = np.array(recognition)
    walk_arr = np.isin(recognition_np, [1,2])
    fall_arr = np.isin(recognition_np, [3,4,5])

#   (3)both     (2)walk     1(fall)
    if np.logical_and(np.any(walk_arr), np.any(fall_arr)): 
        _recognition =3
    elif np.any(walk_arr):
        _recognition = 2
    elif  np.any(fall_arr):
        _recognition=1
    else:
        _recognition = None 

# -------------------------------old--------------------------
# def run():
#     global _abnormal, _bodycount
#     abnormal = _abnormal
#     bodycount = _bodycount
#     result = 0
    
#     if bodycount == 6:
#         result = 0
#     elif (bodycount != 6) and (abnormal == 1):
#         result = 1
#     elif (bodycount != 6) and (abnormal == 0):
#         result = 2 

#     #result = 0(none) 1(fall) 2(walk) 
#     return result
# -------------------------------old--------------------------

def run():
    global _bodycount, _recognition
    bodycount = _bodycount
    recognition = _recognition
    result = 0
    result = recognition
    if bodycount == 6:
        result = 0
        print("None")
        
    elif (bodycount != 6) and (recognition == 1):
        result = 1
        print("Fall")

    elif (bodycount != 6) and (recognition == 2):
        result = 2 
        print("Walk")
        
    elif (bodycount != 6) and (recognition == 3):
        result = 3
        print("both")
    #result = 0(none) 1(fall) 2(walk) 3(both)
    return result


def pubout():
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        abnormal_result_pub.publish(run())
        # print(run())
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('abnormal_result', anonymous=True)
    rospy.Subscriber("/socket/recv", Int32, bodycount_callback)
    # rospy.Subscriber("/socket/abnormal", Int32, abnormal_callback)
    rospy.Subscriber("/action/recognition", Int32MultiArray, recognition_callback)
    abnormal_result_pub = rospy.Publisher('/abnormal_results', Int32, queue_size=10)
    try:
        pubout()
    except rospy.ROSInterruptException:
        pass

