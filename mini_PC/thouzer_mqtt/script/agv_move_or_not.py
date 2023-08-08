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
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

sub_vel = "0/WHISPERER/RMS-10B1-AAJ65/vel2D_DWO"  #vel2D_DWO
json_address = '/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mqtt_api'
vel_params = {}

# ID
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)

# 连接MQTT服务
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT server IP
    MQTTPORT = 1883  # MQTT
    mqttClient.username_pw_set("SmartRobot", "SmartRobot") # mqtt服务器账号密码
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()

def vel_on_message_come(client, userdata, msg):
    global vel_params
    _str = str(msg.payload.decode('gb2312'))
    vel_params = json.loads(_str)
    # print(len(vel_params))

# subscribe
def vel_subscribe():
    global v, w
    mqttClient.subscribe(sub_vel)
    # mqttClient.subscribe([(sub_vel,2), (sub_status,2)])
    mqttClient.on_message = vel_on_message_come 
    if len(vel_params) > 0:
        v = vel_params['v_mps']
        w = vel_params['w_degps']



def run():
    global v, w
    v = 1
    w = 1
    mqtt_connect()
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():


        vel_subscribe()
        
        if (v == 0) and (w == 0):
            move_or_not = 0
        else:
            move_or_not = 1        
        print(move_or_not)
        move_or_not_pub.publish(move_or_not)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('thouzer_disappear', anonymous =True)
    move_or_not_pub = rospy.Publisher("/agv_move_or_not", Int32, queue_size=10)
    try:
        run()
    except rospy.ROSInterruptException:
        pass
