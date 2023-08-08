#!/usr/bin/env python3
import rospy
import socket
import numpy as np
import cv2 
import time
from std_msgs.msg import Int32
import argparse

parser = argparse.ArgumentParser()

def setup(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = (HOST, PORT)
    s.bind(address)  
    s.listen(True)   
    conn, addr = s.accept()
    print ('Waiting for images...')
    return conn, s

if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address", type = str, default = "192.168.0.209") #"192.168.0.215"
    parser.add_argument("--port", help="The server port number", type=int, default = 9000)
    args , unknown = parser.parse_known_args() #for roslaunch

    rospy.init_node('socket_bodyCount', anonymous=True) 
    socketRecv_pub = rospy.Publisher('/socket/recv', Int32, queue_size=1)
    conn,s = setup(args.ip, args.port)
    rate = rospy.Rate(100)
    # while True:
    while not rospy.is_shutdown():
        receive = conn.recv(1).decode('utf-8')
        socketRecv_pub.publish(int(receive))
        rate.sleep()
    s.close()
