#!/usr/bin/env python3
import rospy
import socket


class Hub:
    def __init__(self, sock=None, host='192.168.0.7', port=13000, dataLen=10):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.connect((host, port))
        self.sock.setblocking(False)    
        self.dataLen = dataLen

    def ReadState(self):
        chunks = []
        chunk = None
        while chunk is None:
            try:
                chunk = self.sock.recv(1)
            except socket.error:
                pass
            if chunk is not None:
                if(chunk==b'\n'):
                    break
                chunks.append(chunk)
                chunk = None
        return self.dataToState(b''.join(chunks).decode('utf-8'))

    def dataToState(self, data):
        d = data.split(",")
        for i in range(len(d)):
            d[i] = float(d[i])
        return d

if __name__ == '__main__':
    h = Hub()
    try:
        while True:
            rec = h.ReadState()
            print(rec, '\n')

    except KeyboardInterrupt:
        print("bye")
    except Exception as e:
        print(e)

    