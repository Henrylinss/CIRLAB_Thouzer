from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2 
import numpy as np
import socket
import argparse

parser = argparse.ArgumentParser()

#BGR
SKELETON_COLORS = [(0, 0, 255), #red
                  (0, 128, 255),  #orange
                  (0, 255, 0), #green
                  (255, 0, 0), # blue
                  (128, 0, 128), #purple
                  (203, 192, 255)] #pink

def draw_body_bone(joints, jointPoints, joint0, joint1):
    if (float(jointPoints[joint0].x) == float('inf')) or (float(jointPoints[joint0].x) == float('-inf')) or (float(jointPoints[joint0].y) == float('inf') or (float(jointPoints[joint0].y) == float('-inf'))):
        start = (0, 0)
        end = (0, 0)
        return start, end
    
    elif (float(jointPoints[joint1].x) == float('inf')) or (float(jointPoints[joint1].x) == float('-inf')) or (float(jointPoints[joint1].y) == float('inf') or (float(jointPoints[joint1].y) == float('-inf'))):
        start = (0, 0)
        end = (0, 0)
        return start, end 
    
    else:    
        start = (int(jointPoints[joint0].x), int(jointPoints[joint0].y))
        end = (int(jointPoints[joint1].x), int(jointPoints[joint1].y))  
        return start, end     
     
def draw_body(joints, jointPoints):
    # Torso
    s0, e0 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
    s1, e1 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
    s2, e2 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
    s3, e3 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
    s4, e4 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
    s5, e5 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
    s6, e6 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
    s7, e7 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
    # Right Arm    
    s8, e8 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
    s9, e9 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
    s10, e10 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
    s11, e11 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
    s12, e12 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);
    
    # Left Arm
    s13, e13 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
    s14, e14 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
    s15, e15 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
    s16, e16 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
    s17, e17 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);
    
    # Right Leg
    s18, e18 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
    s19, e19 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
    s20, e20 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);
    
    # Left Leg
    s21, e21 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
    s22, e22 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
    s23, e23 = draw_body_bone(joints, jointPoints, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    s = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23]
    e = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23]
    return s, e

def plt_line(img, s, e, color, index):
    text = f"Character {index}"
    position = (s[0][0]+15, s[0][1]) 
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.line(img, s[0], e[0], color, 5)
    cv2.line(img, s[1], e[1], color, 5)
    cv2.line(img, s[2], e[2], color, 5)
    cv2.line(img, s[3], e[3], color, 5)
    cv2.line(img, s[4], e[4], color, 5)
    cv2.line(img, s[5], e[5], color, 5)
    cv2.line(img, s[6], e[6], color, 5)
    cv2.line(img, s[7], e[7], color, 5)
    cv2.line(img, s[8], e[8], color, 5)
    cv2.line(img, s[9], e[9], color, 5)
    cv2.line(img, s[10], e[10], color, 5)
    cv2.line(img, s[11], e[11], color, 5)
    cv2.line(img, s[12], e[12], color, 5)
    cv2.line(img, s[13], e[13], color, 5)
    cv2.line(img, s[14], e[14], color, 5)
    cv2.line(img, s[15], e[15], color, 5)
    cv2.line(img, s[16], e[16], color, 5)
    cv2.line(img, s[17], e[17], color, 5)
    cv2.line(img, s[18], e[18], color, 5)
    cv2.line(img, s[19], e[19], color, 5)
    cv2.line(img, s[20], e[20], color, 5)
    cv2.line(img, s[21], e[21], color, 5)
    cv2.line(img, s[22], e[22], color, 5)
    cv2.line(img, s[23], e[23], color, 5)    
    return img


if __name__ == '__main__':
    parser.add_argument("--ip", help="The server IP address you want to connect", required=True)
    args = parser.parse_args()  
    _kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)    

    height = 175  #200
    width = 420  # 480

    HOST = '192.168.0.84' #mointor PC
    # HOST = '192.168.0.19' #Heng
    # HOST = '192.168.0.242' #mointor
    
    PORT = 10000
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_server = (args.ip, PORT)
    sock.connect(address_server)   
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]    
    
    while True:   
        frame = _kinect.get_last_color_frame()
        gbra = frame.reshape([_kinect.color_frame_desc.Height, _kinect.color_frame_desc.Width, 4])
        color_frame = gbra[:, :, 0:3]
        colorImg = color_frame.copy() 
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
                        
                    joints = body.joints         
                    joint_points = _kinect.body_joints_to_color_space(joints)
                    s, e = draw_body(joints, joint_points)
                    colorImg_line = plt_line(colorImg, s, e, SKELETON_COLORS[i], i)
                    colorImg_lineResize = cv2.resize(colorImg_line, (width, height))
                    colorImg_encode = cv2.imencode('.jpg', colorImg_lineResize, encode_param)[1]
                    data_encode = np.array(colorImg_encode)
                    str_encode = data_encode.tostring()
                    sock.send(str.encode(str(len(str_encode)).ljust(16)))
                    sock.send(str_encode)
                    print ('Body Frame')
    
                if bodyCount == 6:
                    color_frame_img = cv2.resize(color_frame, (width, height))
                    img_encode = cv2.imencode('.jpg', color_frame_img, encode_param)[1]
                    data_encode = np.array(img_encode)
                    str_encode = data_encode.tostring()       
                    sock.send(str.encode(str(len(str_encode)).ljust(16)))
                    sock.send(str_encode)
                    print ('Color Frame')
        
    _kinect.close()             
    sock.close()

    
    
    
    
    

    

