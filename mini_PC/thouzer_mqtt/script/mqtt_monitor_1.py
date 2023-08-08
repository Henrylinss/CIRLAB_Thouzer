#!/usr/bin/env python3
from paho.mqtt import client as mqtt
import time
import rospy
import numpy as np
import json


topic1 = "0/WHISPERER/RMS-10B1-AAJ65/battery"                   #battery
topic2 = "0/WHISPERER/RMS-10B1-AAJ65/pos2D_DWO"                 #pose2D_DWO
topic3 = "0/WHISPERER/RMS-10B1-AAJ65/vel2D_DWO"                 #vel2D_DWO
topic_MT = "0/THOUZER_HW/RMS-10B1-AAJ65/event/app"              #monitior
topic_SpeedMode = "0/WHISPERER/RMS-10B1-AAJ65/speedmode"        #speedmode

# 生成客户端ID
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)
params = {}
# 连接MQTT服务
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT server IP
    MQTTPORT = 1883  # MQTT
    mqttClient.username_pw_set("smartrobot", "7385smartrobot") # mqtt服务器账号密码
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()



def on_message_come(client, userdata, msg):
    global params
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)
    # print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('gb2312')))



# subscribe
def on_subscribe():
    # mqttClient.subscribe([(topic1,2), (topic2,2),(topic3,2)])
    mqttClient.subscribe([(topic_MT,2)])
    mqttClient.on_message = on_message_come 
    # print(params)
    if len(params) > 0:
        print(params)

def run():
    rospy.init_node('mqtt_subscribe', anonymous =True)
    mqtt_connect()
    rate = rospy.Rate(10) # 1hz
    while not rospy.is_shutdown():
        on_subscribe()
        rate.sleep()

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass