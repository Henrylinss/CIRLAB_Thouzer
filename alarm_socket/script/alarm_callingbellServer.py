#!/usr/bin/env python3
import rospy
import socket
import numpy as np
import cv2 
import time
from std_msgs.msg import Int32
import sys
import selectors
import types
import argparse

HOST = '192.168.0.19'
PORT = 2345

sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            if recv_data.decode():
                data.outb += b"OK"
                command = int(recv_data.decode())
                print("command:",command)
                socketRecv_pub.publish(command)
            else:
                data.outb += b"Wrong command!"
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            # print(f"Send {data.outb!r} to {data.addr}")
            print((recv_data.decode()))
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def server(ip, port):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((ip, port))
    lsock.listen()
    print(f"Listening on {(ip, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while not rospy.is_shutdown():
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt or rospy.ROSInterruptException:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address", required=True)
    parser.add_argument("--port", help="The server port number", type=int, required=True)
    args = parser.parse_args()
    rospy.init_node('socket_Calling_Bell', anonymous=True) 
    socketRecv_pub = rospy.Publisher('/socket/callingBell_status', Int32, queue_size=1) 
    server(args.ip, args.port)
