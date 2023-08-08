#!/usr/bin/env python3
import rospy
import numpy as np
import math
import tf
import argparse
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion
from std_msgs.msg import String

parser = argparse.ArgumentParser()

def amcl_initialpose_pub(pos):
    fixed_frame = String()
    fixed_frame = "map"
    
    if pos == "A":
        x = 20.681
        y = -30.802
        theta = 0
    elif pos == "B":
        x = -2.427
        y = 0.936
        theta = -1.57
    elif pos == "O":
        x = 5.423
        y = -35.042
        theta = 3.122
    elif pos == "Dis":
        x = 21.966
        y = -30.946
        theta = -0.116
    elif pos == "Fall":
        x = 23.461
        y = -27.525
        theta = 1.377

    p = PoseWithCovarianceStamped()
    # p.header.seq = 1
    p.header.frame_id = fixed_frame
    p.header.stamp = rospy.Time.now()

    p.pose.pose.position.x = x
    p.pose.pose.position.y = y
    p.pose.pose.position.z = 0.0

    quat = tf.transformations.quaternion_from_euler(0.0, 0.0, theta)
    p.pose.pose.orientation.x = quat[0]
    p.pose.pose.orientation.y = quat[1]
    p.pose.pose.orientation.z = quat[2]
    p.pose.pose.orientation.w = quat[3]
    p.pose.covariance[6*0+0] = 0.5 * 0.5
    p.pose.covariance[6*1+1] = 0.5 * 0.5
    p.pose.covariance[6*5+5] = math.pi/12.0 * math.pi/12.0

    initialpose_pub.publish(p)
    print("Publish Sucessful")
    print(p)
# type = float

if __name__ == '__main__':
    parser.add_argument("--pos", help="amcl initial pos ", type = str, default = "O")
    # parser.add_argument("--x", help="amcl initial pose x", type = float, default = 20.782)  #ntnu4f_full_v2: A. ntnu4f:cirlab to outside car head to outside(20.679 -11.475 -1.576) 
    # parser.add_argument("--y", help="amcl initial pose y", type = float, default = -30.716)
    # parser.add_argument("--theta", help="amcl initial pose theta", type = float, default = 0)
    args = parser.parse_args()
    rospy.init_node('set_amcl_initial_pose', anonymous = True)
    rate = rospy.Rate(10) # 10hz
    initialpose_pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size=1)
    count = 0
    while count < 5:
        amcl_initialpose_pub(args.pos)
        count += 1
        rate.sleep()
    

