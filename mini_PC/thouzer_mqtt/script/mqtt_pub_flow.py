#!/usr/bin/env python3
from paho.mqtt import client as mqtt
import time
import json
import rospy

client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)

topic_sub = "0/WHISPERER/RMS-10B1-AAJ65/battery"
topic_pub = "0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd"
# connect to MQTT sever
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT IP
    MQTTPORT = 1883  # MQTT port
    mqttClient.username_pw_set("SmartRobot", "SmartRobot") # mqtt server pw
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()



def on_message_come(client, userdata, msg):
    print("Topic:"+msg.topic+" Message:"+str(msg.payload.decode('gb2312')))

def open_json():
    with open('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mqtt_api/pub_flow.json', 'r') as read_file:
        api = json.load(read_file)
    return api

# subscribe 
def on_subscribe():
    mqttClient.subscribe(topic_sub, 2)
    mqttClient.on_message = on_message_come  

def on_publish():
    msg = str(open_json())
    msg = msg.replace("'",'"')
    mqttClient.publish(topic_pub, f'{msg}')
    
def run():
    rospy.init_node('mqtt_pub_test', anonymous =True)
    mqtt_connect()
    rate = rospy.Rate(10) # 10hz
    on_publish()
    while not rospy.is_shutdown():
        # on_publish()
        rate.sleep()



if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass



