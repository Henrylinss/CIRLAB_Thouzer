#!/usr/bin/env python3
import time
import rospy
import numpy as np
import tf
import json
from std_msgs.msg import Float64, String, Int32
import sys
import socket
import selectors
import types
import argparse


sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser()

_path = ["path","function"]
_status = 0
_abnormal_data = 0
_bodycount = 0
_move_or_not = 0
# socket client
def client(ip, port, command):
    server_addr = (ip, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_addr)
        print(f"Connect to {server_addr}")

        s.sendall(command.encode())
        print(f"Send command: {command}")

        data = s.recv(1024)
        print(f"Receive: {data.decode()}")

def bodycount_callback(bodycount_data):
    global  _bodycount
    _bodycount = bodycount_data.data
    # print("_bodycount:",_bodycount)

def abnormal_callback(abnormal_data):
    global _abnormal_data
    _abnormal_data = abnormal_data.data

def status_callback(status_data):
    global _status
    _status = status_data.data
    # print("_status:",_status)

def move_or_not_callback(move_or_not_data):
    global _move_or_not
    _move_or_not = move_or_not_data.data

def path_callback(path_data):
    global _path
    path_list = ["OA", "OB", "AO", "AB", "BA", "BO", "WA", "OW", "M3"]
    function_list = ["follow", "end_follow", "hold", "resume", "water_brought"]
    path = path_data.data
    if path in path_list:
        _path[0] = path
        _path[1] = "MT"
    elif path in function_list:
        _path[1] = path
    # print("_path:",_path)


# run 
def run(ip, port):
    global _path, _status, _abnormal_data, _bodycount, _move_or_not
    rate = rospy.Rate(10) # 10hz
    count = True
    while not rospy.is_shutdown():
        path = _path
        status = _status
        abnormal_result  = _abnormal_data
        bodycount = _bodycount
        move_or_not = _move_or_not
        print("-----------------------")
        print("path:",path)
        print("status:",status)
        print("bodycount:",bodycount)
        print("count",count)
        print("-----------------------")

# status = 2(memoryTrace) ,5(memoryTraceResume)
        if ((status == 2) or (status == 5)) and (path[0] == "M3"):
            if (abnormal_result == 1) or (abnormal_result == 2) or (bodycount !=6):
                if (path[1] != "hold") and (count == True):
                    client(ip, port, "self_move_hold")
                    print("client: self_move_hold")
                    count = False
                
        elif (path[1] == "hold") and (path[0] == "M3") and (move_or_not == 0):
            if abnormal_result == 0:
                count = True 
        
        rate.sleep()



if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address you want to connect", required=True)
    parser.add_argument("--port", help="The server port number listend", type=int, required=True)
    args , unknown = parser.parse_known_args() #for roslaunch

    rospy.init_node('thouzer_demo3', anonymous =True)
    rospy.Subscriber("/agv_status", Int32, status_callback)
    rospy.Subscriber("/memorytrace_path", String, path_callback)
    rospy.Subscriber("/socket/recv", Int32, bodycount_callback)
    rospy.Subscriber("/agv_move_or_not", Int32, move_or_not_callback)
    rospy.Subscriber("/abnormal_results", Int32, abnormal_callback)
    
    try:
        run(args.ip, args.port)
    except rospy.ROSInterruptException:
        pass
