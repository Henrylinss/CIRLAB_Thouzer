#!/usr/bin/env python3
from paho.mqtt import client as mqtt
import time
import json
import rospy
import os
import sys
import termios

# 生成客户端ID
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)

topic_sub = "0/WHISPERER/RMS-10B1-AAJ65/battery"
topic_pub_MT_play = "0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd"

play_back_json = '/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mqtt_api/pub_memoryTrace_playBack.json'
# 连接MQTT服务
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT服务器地址
    MQTTPORT = 1883  # MQTT端口
    mqttClient.username_pw_set("SmartRobot", "SmartRobot") # mqtt服务器账号密码
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()


# 消息处理函数
def on_message_come(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('gb2312')))

def open_json():
    with open('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mqtt_api/pub_memoryTrace_hold.json', encoding="utf-8") as read_file:  #encoding="utf-8" replace 'r'
        api = json.load(read_file)
    return api

# subscribe 消息
def on_subscribe():
    mqttClient.subscribe(topic_sub, 2)
    mqttClient.on_message = on_message_come  # 消息到来处理函数

def on_publish():
    msg = str(open_json())
    msg = msg.replace("'",'"')
    print(msg)
    mqttClient.publish(topic_pub_MT_play, f'{msg}')


def press_any_key_exit(msg):

    fd = sys.stdin.fileno()

    old_ttyinfo = termios.tcgetattr(fd)
    new_ttyinfo = old_ttyinfo[:]
    new_ttyinfo[3] &= ~termios.ICANON
    new_ttyinfo[3] &= ~termios.ECHO

    sys.stdout.write(msg)
    sys.stdout.flush()

    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)

    os.read(fd, 7)
    termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)
    
def run():
    rospy.init_node('mqtt_pub_MT_hold', anonymous =True)
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