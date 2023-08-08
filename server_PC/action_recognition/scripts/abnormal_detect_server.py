#!/usr/bin/env python3
import socket
import rospy
import numpy as np
import cv2
from std_msgs.msg import Int32
# 創建一個 socket 對象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 取得本地主機名
# host = socket.gethostname()
host = "192.168.0.209"

port = 9000

# 綁定端口
serversocket.bind((host, port))

# 設置最大連接數，超過後排隊
serversocket.listen(5)
if __name__ == '__main__':
    rospy.init_node('socket_abnormal', anonymous=True)
    socketRecv_pub = rospy.Publisher('/socket/abnormal', Int32, queue_size=1)
    rate = rospy.Rate(100)
    
    while not rospy.is_shutdown():
        # 建立客戶端連接
        clientsocket, addr = serversocket.accept()

        print("連接地址: %s" % str(addr))

        # 接收客戶端傳來的數據，最大為1024個字節
        data = clientsocket.recv(1024)

        # 解碼為字符串
        message = data.decode('utf-8')
        socketRecv_pub.publish(int(message))
        print("接收到的消息: ", message)

        clientsocket.close()
        rate.sleep()

    serversocket.close()