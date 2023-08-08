#!/usr/bin/env python3
import sys
import socket
import selectors
import types
import argparse
from paho.mqtt import client as mqtt
import time
import rospy
import numpy as np
import json
from std_msgs.msg import Int32

sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser()
messages = [b"Message 1 from client.", b"Message 2 from client."]

rospy.init_node('report_agv', anonymous =True)


topic_sub = "0/WHISPERER/RMS-10B1-AAJ65/app_status"  

json_address = '/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mqtt_api'

client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)
params ={}
# connect mqtt
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT server IP
    MQTTPORT = 1883  # MQTT
    mqttClient.username_pw_set("SmartRobot", "SmartRobot") # mqtt username, pwd
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  
    mqttClient.loop_start()



def on_message_come(client, userdata, msg):
    global params
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)
    # print("Topic:"+msg.topic+" Message:" + str(msg.payload.decode('gb2312')))



# subscribe
def on_subscribe():
    mqttClient.subscribe([(topic_sub,2)])
    mqttClient.on_message = on_message_come 
    # print(params)

    if len(params) > 0:
        app = params["app"]
        print("app:", app)
        print("----------")
        return app

def run(ip,port):
    command = 0
    mqtt_connect()
    rate = rospy.Rate(20) # 10hz
    ros_pub = rospy.Publisher('/agv_status', Int32, queue_size = 10)
    while not rospy.is_shutdown():
        app_status = on_subscribe()
        if app_status == '#alert':  # agv shut down 
            command = 1
            ros_pub.publish(command)
            # time.sleep(1)
            client(ip,port) 
            
        elif app_status == './bin/app-memorytrace': # donig memorytrace
            command = 2
            ros_pub.publish(command)
        elif app_status == '#start': # 
            command = 3
            ros_pub.publish(command)
        elif app_status == '#success': # memorytrace done
            command = 4
            ros_pub.publish(command)
        elif app_status == './bin/app-memorytraceResume':
            command = 5
            ros_pub.publish(command)
        else:
            command = 0
            ros_pub.publish(command)
        print("status: ", command)
            
        rate.sleep()
# ---------------------------------------------------------------------


def client(ip, port):
    server_addr = (ip, port)
    command = 'agv_shut_down'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_addr)
        print(f"Connect to {server_addr}")

        s.sendall(command.encode())
        print(f"Send command: {command}")

        data = s.recv(1024)
        print(f"Receive: {data.decode()}")


if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address you want to connect", required=True)
    parser.add_argument("--port", help="The server port number listend", type=int, required=True)
    # parser.add_argument("--command", help="The command you want to send to server", required=True)
    args = parser.parse_args()
    
    try:
        run(args.ip, args.port)
    except rospy.ROSInterruptException:
        pass
