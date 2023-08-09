from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import socket
import time
import argparse

parser = argparse.ArgumentParser()

if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address you want to connect", required=True)
    args = parser.parse_args()
    _kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)    
    
    # HOST = '192.168.0.19'# Heng
    # HOST = '192.168.0.242' #mointor
    HOST = '192.168.0.84' #mointor PC
    PORT = 9000
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_server = (args.ip, PORT)
    sock.connect(address_server)    
    
    while True:   
        bodyCount = 0
        if _kinect.has_new_body_frame():
            _bodies = _kinect.get_last_body_frame()
            if _bodies is not None: 
                for i in range(0, _kinect.max_body_count):
                    body = _bodies.bodies[i]
                    if not body.is_tracked: 
                        bodyCount += 1
                        continue 
                        bodyCount -= 1                
                sock.send(str(bodyCount).encode('utf-8'))
                print (bodyCount)
        time.sleep(0.025)
    _kinect.close()             
    sock.close()