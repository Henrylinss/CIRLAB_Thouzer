#!/usr/bin/env python3
import rospy
import socket
import numpy as np
import cv2 
import time
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

HOST = '192.168.0.84'
# HOST = '10.8.0.4'
PORT = 10000

def recv_size(sock, count):
     buf = b''
     while count:
         newbuf = sock.recv(count)     
         if not newbuf: return None
         buf += newbuf
         count -= len(newbuf)
     return buf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = (HOST, PORT)
s.bind(address)  
s.listen(True)   
print ('Waiting for images...')

conn, addr = s.accept()

if __name__ == '__main__':
    rospy.init_node('socket_image', anonymous=True) 
    kinectv2Image_pub = rospy.Publisher('/kinectv2/image', Image, queue_size=1) 
    bridge = CvBridge()
    rate = rospy.Rate(40)
    # while True:
    while not rospy.is_shutdown():
        length = recv_size(conn, 16)   
        stringData = recv_size(conn,int(length))
        data = np.fromstring(stringData, dtype='uint8')
        decimg_BGR = cv2.imdecode(data, 1)
        decimg_RGB = cv2.cvtColor(decimg_BGR, cv2.COLOR_BGR2RGB)
        decimg_RGB = cv2.flip(decimg_RGB,1)
        image_message = bridge.cv2_to_imgmsg(decimg_RGB, 'rgb8')
        kinectv2Image_pub.publish(image_message)
        rate.sleep()
    s.close()
       
