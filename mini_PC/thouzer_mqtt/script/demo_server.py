#!/usr/bin/env python3
import socket
from paho.mqtt import client as mqtt
import sys
import time
import json
import rospy
import types
import argparse
import selectors
from pydub import AudioSegment
from pydub.playback import play
from std_msgs.msg import String

#load API sound
# audio_start_agv_follow = AudioSegment.from_file('/home/thouzer/python_code/API_sound/start_agv_follow.m4a')
# audio_end_agv_follow = AudioSegment.from_file('/home/thouzer/python_code/API_sound/end_agv_follow.m4a')
# audio_self_move_AO = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_AO.m4a')
# audio_self_move_OA = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_OA.m4a')
# audio_self_move_OB = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_OB.m4a')
# audio_self_move_hold = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_hold.m4a')
# audio_self_move_resume = AudioSegment.from_file('/home/thouzer/python_code/API_sound/self_move_resume.m4a')
# audio_agv_debug = AudioSegment.from_file('/home/thouzer/python_code/API_sound/AGV_debug.m4a')

# audio_arrived_B = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/arrived_B.mp3')
# audio_arrived_O = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/arrived_O.mp3')
# audio_arrived_W = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/arrived_W.mp3')
# audio_start_move_to_W = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_move_to_W.mp3')
# audio_start_move_to_O = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_move_to_O.mp3')
# audio_start_move_to_B = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_move_to_B.mp3')
# audio_plz_to_A = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/plz_to_A.mp3')

audio_start_agv_follow = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/start_agv_follow.mp3')
audio_end_agv_follow = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/end_agv_follow.mp3')
audio_want_water = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/want_water.m4a')
#audio_water_brought = AudioSegment.from_file('/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mp3/water_brought.mp3')

sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser()

#create Mqtt client ID
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)

#API topic
topic_sub = "0/WHISPERER/RMS-10B1-AAJ65/battery"
topic_pub = "0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd"

command_list = ["start_agv_follow", "end_agv_follow", "self_move_hold", "self_move_resume","AGV_debug", "self_move_AO","self_move_OA","self_move_OB","self_move_BO","self_move_AB","self_move_BA", "AGV_debug","self_move_DO", "self_move_OW", "self_move_WA","agv_shut_down", "want_water","self_move_M3"]

# ROS node


api_address = '/home/thouzer/catkin_ws/src/thouzer_mqtt/script/mqtt_api'

#public variable
msg_path = "XX"

# connect MQTT server
def mqtt_connect():
    MQTTHOST = "192.168.212.1"  # MQTT ip
    MQTTPORT = 1883  # MQTT port
    mqttClient.username_pw_set("SmartRobot", "SmartRobot") # mqtt server pw
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)  # 超时时间为60秒
    mqttClient.loop_start()


def on_message_come(client, userdata, msg):
    print("Topic:"+msg.topic+" Message:"+str(msg.payload.decode('gb2312')))

def open_json():
    with open(api_address + '/pub_flow.json', 'r') as read_file:
        api1 = json.load(read_file)
    return api1

def open_json_2():
    with open(api_address + '/mode_cancel.json', 'r') as read_file:
        api2 = json.load(read_file)
    return api2

# def open_json_3():
#     with open(api_address + '/pub_memoryTrace_playBack.json', 'r') as read_file:
#         api3 = json.load(read_file)
#     return api3

def open_json_4():
    with open(api_address + '/pub_memoryTrace_hold.json', 'r') as read_file:
        api4 = json.load(read_file)
    return api4

# def open_json_5():
#     with open(api_address + '/pub_memoryTrace_resume.json', 'r') as read_file:
#         api5 = json.load(read_file)
#     return api5

def open_json_6():
    with open(api_address + '/control_command_start.json', 'r') as read_file:
        api6 = json.load(read_file)
    return api6

def open_json_7():
    with open(api_address + '/stop_control.json', 'r') as read_file:
        api7 = json.load(read_file)
    return api7
#------------------------------------------------------------

def self_move(path):
    global msg_path
    with open(api_address + '/pub_memoryTrace_playBack.json', 'r') as read_file:
        api3 = json.load(read_file)
    msg = str(api3)
    msg = msg.replace("'",'"')
    msg_path = path[10] + path[11]
    msg = msg.replace("XXX",change_path(msg_path))
    print(msg)
    mqtt_connect()
    mqttClient.publish(topic_pub, f'{msg}')

def self_move_resume():
    global msg_path
    with open(api_address + '/pub_memoryTrace_resume.json', 'r') as read_file:
        api5 = json.load(read_file)
    msg = str(api5)
    msg = msg.replace("'",'"')
    msg = msg.replace("XXX",change_path(msg_path))
    mqtt_connect()
    mqttClient.publish(topic_pub, f'{msg}')

def change_path(path):
    if path == "OA":
        return "201"
    elif path == "AO":
        return "202"
    elif path == "OB":
        return "203"
    elif path == "BA":
        return "204"
    elif path == "AB":
        return "205"
    elif path == "BO":
        return "206"
    
    elif path == "OW":
        return "207"
    elif path == "WA":
        return "208"
    elif path == "DO":
        return "209"
        
    elif path == "M3":
        return "107"

    # if path == "OA":
    #     return "301"
    # elif path == "AO":
    #     return "302"
    # elif path == "OB":
    #     return "303"
    # elif path == "BA":
    #     return "304"
    # elif path == "AB":
    #     return "305"
    # elif path == "BO":
    #     return "306"

    # elif path == "OW":
    #     return "307"
    # elif path == "WB":
    #     return "308"
    # elif path == "DO":
    #     return "309"

    # elif path == "M3":
    #     return "310"
#------------------------------------------------------------
def on_publish():
    msg = str(open_json())
    msg = msg.replace("'",'"')
    mqttClient.publish(topic_pub, f'{msg}')

def on_publish_cancel():
    msg = str(open_json_2())
    msg = msg.replace("'",'"')
    mqttClient.publish(topic_pub, f'{msg}')

# def publish_self_move():
#     msg = str(open_json_3())
#     msg = msg.replace("'",'"')
#     mqttClient.publish(topic_pub, f'{msg}')  

def publish_self_move_hold():
    msg = str(open_json_4())
    msg = msg.replace("'",'"')
    mqttClient.publish(topic_pub, f'{msg}')   

# def publish_self_move_resume():
#     msg = str(open_json_5())
#     msg = msg.replace("'",'"')
#     mqttClient.publish(topic_pub, f'{msg}')   

def publish_control_command():
    msg_control = str(open_json_6())
    msg_control = msg_control.replace("'",'"')
    mqttClient.publish(topic_pub, f'{msg_control}')

    
def publish_Inputhibit():
    msg_Inputhibit = str(open_json_7())
    msg_Inputhibit = msg_Inputhibit.replace("'",'"')
    mqttClient.publish(topic_pub, f'{msg_Inputhibit}')
#--------------------------------------------------------------------
    
def start_agv_follow():
    mqtt_connect()
    rate = rospy.Rate(10) # 10hz
    on_publish()


def end_agv_follow():
    mqtt_connect()
    rate = rospy.Rate(10) # 10hz
    on_publish_cancel()

# def self_move():
#     mqtt_connect()
#     rate = rospy.Rate(10) # 10hz
#     publish_self_move()

def self_move_hold():
    mqtt_connect()
    rate = rospy.Rate(10) # 10hz
    publish_self_move_hold()

# def self_move_resume():
#     mqtt_connect()
#     rate = rospy.Rate(10) # 10hz
#     publish_self_move_resume()

def AGV_debug():
    mqtt_connect()
    # rate = rospy.Rate(10) # 10hz
    publish_control_command()
    time.sleep(2)
    publish_Inputhibit()
#----------------------------------------------------------------
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    global path_
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            if recv_data.decode() in command_list:
                data.outb += b"OK"
                if recv_data.decode() =="start_agv_follow":
                    start_agv_follow()
                    path_ = "follow"
                    path_pub.publish(path_)
                    play(audio_start_agv_follow)
                    
                elif recv_data.decode() =="end_agv_follow":
                    end_agv_follow()
                    path_ = "end_follow"
                    path_pub.publish(path_)
                    play(audio_end_agv_follow)
                
                elif recv_data.decode() == "self_move_AO":
                    self_move(recv_data.decode())
                    path_ = "AO"
                    path_pub.publish(path_)
                    # play(audio_start_move_to_O)
                
                elif recv_data.decode() == "self_move_OA":
                    self_move(recv_data.decode())
                    path_ = "OA"
                    path_pub.publish(path_)
                    # play(audio_self_move_OA)
                
                elif recv_data.decode() == "self_move_BO":
                    self_move(recv_data.decode())
                    path_ = "BO"
                    path_pub.publish(path_)
                    # play(audio_start_move_to_O)
                
                elif recv_data.decode() == "self_move_OB":
                    self_move(recv_data.decode())
                    path_ = "OB"
                    path_pub.publish(path_)
                    # play(audio_self_move_BO)
                    # paly(audio_start_move_to_B)

                elif recv_data.decode() == "self_move_AB":
                    self_move(recv_data.decode())
                    path_ = "AB"
                    path_pub.publish(path_)
                    # play(audio_self_move_AB)
                    # paly(audio_start_move_to_B)

                elif recv_data.decode() == "self_move_BA":
                    self_move(recv_data.decode())
                    path_ = "BA"
                    path_pub.publish(path_)
                    # play(audio_self_move_BA)

                elif recv_data.decode() == 'self_move_DO':
                    self_move(recv_data.decode())
                    path_ = "DO"
                    path_pub.publish(path_)

                elif recv_data.decode() =="self_move_M3":
                    self_move(recv_data.decode())
                    path_ = "M3"
                    path_pub.publish(path_)
                elif recv_data.decode() == "self_move_OW":
                    self_move(recv_data.decode())
                    path_ = "OW"
                    path_pub.publish(path_)

                elif recv_data.decode() == "self_move_WA":
                    self_move(recv_data.decode())
                    path_ = "WB"
                    path_pub.publish(path_)

                elif recv_data.decode() =="self_move_hold":
                    self_move_hold()
                    path_ = "hold"
                    path_pub.publish(path_)
                    # play(audio_self_move_hold)
                
                elif recv_data.decode() =="self_move_resume":
                    self_move_resume()
                    path_ = "resume"
                    path_pub.publish(path_)
                    # play(audio_self_move_resume)
        
                # elif recv_data.decode() == "AGV_debug":
                elif recv_data.decode() == "AGV_debug":#()agv_shut_down
                    time.sleep(5)
                    AGV_debug()
                    # play(audio_agv_debug)

                elif recv_data.decode() == "want_water":
                    play(audio_want_water)

                #elif recv_data.decode() =="water_brought":
                    #play(audio_water_brought)
            else:
                data.outb += b"Wrong command!"
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Send {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def server(ip, port):
    global path_
    port_ = ""
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((ip, port))
    lsock.listen()
    print(f"Listening on {(ip, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    rate = rospy.Rate(5)
    try:
        while not rospy.is_shutdown():
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)

                    rate.sleep()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()
#----------------------------------------------------------------
if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address", required=True)
    parser.add_argument("--port", help="The server port number", type=int, required=True)
    args = parser.parse_args()
    rospy.init_node('thouzer_server', anonymous =True)
    path_pub = rospy.Publisher('/memorytrace_path', String, queue_size=10)
    server(args.ip, args.port)
    



