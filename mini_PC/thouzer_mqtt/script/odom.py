#!/usr/bin/env python3
import time
import rospy
import numpy as np
import math
import tf
import json
from paho.mqtt import client as mqtt
from math import sin, cos, pi
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

#topic
topic1 = "0/WHISPERER/RMS-10B1-AAJ65/battery"    #battery
topic2 = "0/WHISPERER/RMS-10B1-AAJ65/pos2D_DWO"  #pose2D_DWO
topic3 = "0/WHISPERER/RMS-10B1-AAJ65/vel2D_DWO"  #vel2D_DWO

rospy.init_node('mqtt_odom_test', anonymous =True)
rate = rospy.Rate(10) # 10hz
odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
odom_broadcaster = tf.TransformBroadcaster()

yaw_deg = 0
x_m = 0
y_m = 0
# 生成客户端ID
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)
params = {}

# 连接MQTT服务
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT server IP
    MQTTPORT = 1883  # MQTT
    mqttClient.username_pw_set("SmartRobot", "SmartRobot") # mqtt服务器账号密码
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()


def on_message_come(client, userdata, msg):
    global params
    _str = str(msg.payload.decode('gb2312'))# 'gb2312'decode number
    params = json.loads(_str)


# subscribe
def on_subscribe():
    global yaw_deg,x_m,y_m 
    # mqttClient.subscribe([(topic1,2), (topic2,2),(topic3,2)])
    mqttClient.subscribe([(topic2,2)])
    mqttClient.on_message = on_message_come 

    if len(params) > 0:
        if len(params) == 6:        #pose2D_DWO
            x_m = params['x_m']
            y_m = params['y_m']
            yaw_deg = params['yaw_deg']
            tDist_m = params['tDist_m']
            tAngle_deg = params['tAngle_deg']
            print("x_m: ",x_m)
            print("y_m: ",y_m)
            print("yaw_deg: ",yaw_deg)
            print("tDist_m: ",tDist_m)
            print("tAngle_deg", tAngle_deg)
            print("------")

def run():
    global yaw_deg,x_m,y_m 
    mqtt_connect()

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        on_subscribe()

        #converted from deg to radian
        yaw = yaw_deg * (math.pi / 180)
        
        # since all odometry is 6DOF we'll need a quaternion created from yaw
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, yaw)
        # first, we'll publish the transform over tf
        odom_broadcaster.sendTransform(
            (x_m, y_m, 0),
            odom_quat,
            current_time,
            "base_link",
            "odom"
        )

        # next, we'll publish the odometry message over ROS
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"

        # set the position
        odom.pose.pose = Pose(Point(x_m, y_m, 0.), Quaternion(*odom_quat))


        # publish the message
        odom_pub.publish(odom)

        last_time = current_time
        rate.sleep()

if __name__ == '__main__':

    try:
        run()
    except rospy.ROSInterruptException:
        pass