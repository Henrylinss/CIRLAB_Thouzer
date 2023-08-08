#!/usr/bin/env python3
import time
import rospy
import numpy as np
import math
import tf
import json
from paho.mqtt import client as mqtt
from math import sin, cos, pi
from std_msgs.msg import Float64, String, Int32
from pydub import AudioSegment
from pydub.playback import play
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, PoseWithCovarianceStamped, PoseStamped
import sys
import socket
import selectors
import types
import argparse

#load API sound
# audio_start_agv_follow = AudioSegment.from_file('/home/thouzer/python_code/API_sound/start_agv_follow.m4a')
# audio_end_agv_follow = AudioSegment.from_file('/home/thouzer/python_code/API_sound/end_agv_follow.m4a')
# audio_self_move_AO = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_AO.m4a')
# audio_self_move_OA = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_OA.m4a')
# audio_self_move_OB = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_OB.m4a')
# audio_self_move_hold = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_hold.m4a')
# audio_self_move_resume = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_resume.m4a')
# audio_agv_debug = AudioSegment.from_file('/home/thouzer/python_code/API_sound/AGV_debug.m4a')
audio_arrived_B = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/arrived_B.mp3')
audio_arrived_O = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/arrived_O.mp3')
audio_arrived_W = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/arrived_W.mp3')
audio_start_move_to_W = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_move_to_W.mp3')
audio_start_move_to_O = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_move_to_O.mp3')
audio_start_move_to_B = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_move_to_B.mp3')
audio_start_agv_follow = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_agv_follow.mp3')
audio_end_agv_follow = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/end_agv_follow.mp3')
audio_plz_to_A = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/plz_to_A.mp3')
# audio_plz_to_311 = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/plz_to_311.mp3')
audio_water_brought = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/water_brought.mp3')

sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser()
messages = [b"Message 1 from client.", b"Message 2 from client."]

_path = ["path","function"]
_status = 0


def client(ip, port):
    server_addr = (ip, port)
    command = 'wrong_relay_point'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_addr)
        print(f"Connect to {server_addr}")

        s.sendall(command.encode())
        print(f"Send command: {command}")

        data = s.recv(1024)
        print(f"Receive: {data.decode()}")


def status_callback(status_data):
    global _status
    _status = status_data.data

def path_callback(path_data):
    global _path
    path_list = ["OA", "OB", "AO", "AB", "BA", "BO", "WA", "OW", "DO"]
    function_list = ["follow", "end_follow", "hold", "resume", "water_brought"]
    path = path_data.data
    if path in path_list:
        _path[0] = path
        _path[1] = "MT"
    elif path in function_list:
        _path[1] = path




def pose_callback(pose_msg):
    global x, y
    x = pose_msg.pose.pose.position.x
    y = pose_msg.pose.pose.position.y

def near_A_or_B():
    global x, y
    
    # -----ntnu-------
    ax = 20.782
    ay = -30.716

    ox = 5.423
    oy = -35.042
    # -----ntnu-------

    # #-----hsinchu----
    # ax = -2.977
    # ay = 28.183

    # ox = 3.89
    # oy = 33.925
    # #-----hsinchu----

    dis_a = math.sqrt((x-ax)**2 + (y-ay)**2)
    dis_o = math.sqrt((x-ox)**2 + (y-oy)**2)
    if dis_a > dis_o:
        return "o"
    else:
        return "a"

def run():
    global _path, _status
    rate = rospy.Rate(10) # 10hz
    count = True
    while not rospy.is_shutdown():
        path = _path
        status = _status
        print(path,status)
        # print("aa")
    # plz take agv to nearlist state
        if (status == 1 ):
            # print(near_A_or_B())
            if (path[1] != "follow") and (path[1] != "end_follow"):
                
                
                play(audio_plz_to_A)
                count = True
            
        else:
            # arrived audio
            if (status == 4):
                if path[1] == "MT" or path[1] == "resume":
                    if (path[0] == "OB") or (path[0] == "AB"):
                        if count == False:
                            play(audio_arrived_B)
                            count = True

                    elif (path[0] == "AO") or (path[0] == "BO"):
                        if count == False:
                            play(audio_arrived_O)
                            count = True

                    elif (path[0] == "OW"):
                        if count == False:
                            play(audio_arrived_W)
                            count = True

                    elif (path[0] == "WA"):
                        if count == False:
                            play(audio_water_brought)
                            count = True

            # agv start 
            elif (status == 2):
                if path[1] == "MT":
                    if (path[0] == "OB") or (path[0] == "AB"):
                        if count:
                            play(audio_start_move_to_B)
                            count = False

                    elif (path[0] == "AO") or (path[0] == "BO"):
                        if count:
                            play(audio_start_move_to_O)
                            count = False

                    elif (path[0] == "OW"):
                        if count:
                            play(audio_start_move_to_W)
                            count = False
                    
                    elif (path[0] == "WA"):
                        if count:
                            count = False
        rate.sleep()




if __name__ == '__main__':
    #parser.add_argument("--ip", help="The server IP address you want to connect", required=True)
    #parser.add_argument("--port", help="The server port number listend", type=int, required=True)
    #args = parser.parse_args()

    rospy.init_node('thouzer_audio_report', anonymous =True)
    rospy.Subscriber("/agv_status", Int32, status_callback)
    rospy.Subscriber("/memorytrace_path", String, path_callback)
    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, pose_callback)
    try:
        run()
    except rospy.ROSInterruptException:
        pass
