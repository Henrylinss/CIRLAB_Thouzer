#!/usr/bin/env python3
import time
import rospy
import numpy as np
import math
import tf
import json
from paho.mqtt import client as mqtt
from math import sin, cos, pi
from std_msgs.msg import Float64, String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


topic1 = "0/WHISPERER/RMS-10B1-AAJ65/battery"    #battery
topic2 = "0/WHISPERER/RMS-10B1-AAJ65/pos2D_DWO"  #pose2D_DWO
topic3 = "0/WHISPERER/RMS-10B1-AAJ65/vel2D_DWO"  #vel2D_DWO


rospy.init_node('mqtt_sub_vel2D', anonymous =True)
rate = rospy.Rate(10) # 10hz
# vth_pub = rospy.Publisher("odom", Odometry, queue_size=50)
vth_pub = rospy.Publisher("thouzer_vth", Float64, queue_size=50)
# odom = Odometry()
w_degps = 0

# ID
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
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)

# subscribe
def on_subscribe():
    global v_mps,w_degps
    mqttClient.subscribe(topic3, 2)
    # mqttClient.subscribe([(topic3,2), (topic2,2)])
    mqttClient.on_message = on_message_come 
    if len(params) > 0:
        # v = params['v_mps']
        w_degps = params['w_degps']
        # print("w: ",w_degps)
        # print("------")


def run():
    global w_degps
    mqtt_connect()
    

    while not rospy.is_shutdown():
        vth = w_degps * (math.pi / 180)
        # odom.twist.twist.angular.z = vth
        on_subscribe()

        # vth_pub.publish(odom)
        vth_pub.publish(vth)

        rate.sleep()


if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass