#!/usr/bin/env python3
import rospy
import numpy as np
import math
import tf
import argparse
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion
from std_msgs.msg import String

parser = argparse.ArgumentParser()

def amcl_initialpose_pub(x, y, theta):
    fixed_frame = String()
    fixed_frame = "map"

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
    # parser.add_argument("--x", help="amcl initial pose x", type = float, default = 20.679)  #cirlab to outside car head to outside 5.423 -35.042 3.122
    # parser.add_argument("--y", help="amcl initial pose y", type = float, default = -11.475)
    # parser.add_argument("--theta", help="amcl initial pose theta", type = float, default = -1.576)
    parser.add_argument("--x", help="amcl initial pose x", type = float, default = 5.423)  #cirlab to outside car head to outside 5.423 -35.042 3.122
    parser.add_argument("--y", help="amcl initial pose y", type = float, default = -35.042)
    parser.add_argument("--theta", help="amcl initial pose theta", type = float, default = 3.122)
    args = parser.parse_args()
    rospy.init_node('set_amcl_initial_pose', anonymous = True)
    rate = rospy.Rate(10) # 10hz
    initialpose_pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size=1)
    count = 0
    while count < 5:
        amcl_initialpose_pub(args.x, args.y, args.theta)
        count += 1
        rate.sleep()
    

