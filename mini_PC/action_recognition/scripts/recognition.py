#!/usr/bin/env python3
import rospy
import skeleton
import numpy as np
import time
import mfnn
from std_msgs.msg import Int32MultiArray, Int32
from socket_clinet import Hub
from collections import deque

count = 0

class Filter_multiple:
    def __init__(self):
        self.filter_que = deque(maxlen=ske.slidingRange)

    def pre_filer(self, p):
        self.filter_que.append(p)      
        if len(self.filter_que) == self.filter_que.maxlen:
            p = Filter_multiple.majorityElement(self)
        else:
            p = -1        
        return p
    
    def majorityElement(self):
        res, cnt, l = self.filter_que[0], 1, len(self.filter_que)
        for i in range(1, l):
            if res == self.filter_que[i]:
                cnt += 1
            elif cnt > 0:
                cnt -= 1
            else:
                res = self.filter_que[i]                
                cnt += 1
        return res
    
def recognize(w):
    Data = ske.fullDataConvertToTargetData(w)   
    data = ske.predictFast_ontime_fnn(Data)     
    answer, psi_sets = mfnn.prediction_mfnn_ontime(data, weight, index)
    p = np.where(answer==np.max(answer))
    return p

def Recv_Callback(msg):
    global count
    count = msg.data
    actionID = Int32MultiArray()
    if count == 6:
        actionID.data = [datasetFileEn[-1], datasetFileEn[-1], datasetFileEn[-1],
                        datasetFileEn[-1], datasetFileEn[-1], datasetFileEn[-1]]
        actionRecognition_pub.publish(actionID)

if __name__ == "__main__": 
    rospy.init_node('recognition', anonymous=True) 
    actionRecognition_pub = rospy.Publisher('/action/recognition', Int32MultiArray, queue_size=1)  
    rospy.Subscriber('/socket/recv', Int32, Recv_Callback, queue_size=1)
    weight = np.load(mfnn.weight_path, allow_pickle=True)
    index = mfnn.create_rule_index()       
    ske = skeleton.GetSkeletonWithDir(mfnn.ske_path, skeleton.skeleton)
    datasetFileEn = [1, 2, 3, 4, 5, 6]
    actionID1 = Int32MultiArray()
    rate = rospy.Rate(40)
    m = Hub(host="192.168.0.7", port=13000, dataLen=10)
    window0 = deque(maxlen=ske.slidingRange)
    window1 = deque(maxlen=ske.slidingRange)
    window2 = deque(maxlen=ske.slidingRange)
    window3 = deque(maxlen=ske.slidingRange) 
    window4 = deque(maxlen=ske.slidingRange)
    window5 = deque(maxlen=ske.slidingRange)
    
    filter0 = Filter_multiple()  
    filter1 = Filter_multiple()  
    filter2 = Filter_multiple()  
    filter3 = Filter_multiple()  
    filter4 = Filter_multiple()  
    filter5 = Filter_multiple()   

    while not rospy.is_shutdown():
        rec = m.ReadState()
        
        check_people_ind0 = np.all(np.array(rec[0:75]) == 0)
        check_people_ind1 = np.all(np.array(rec[75:150]) == 0)
        check_people_ind2 = np.all(np.array(rec[150:225]) == 0)
        check_people_ind3 = np.all(np.array(rec[225:300]) == 0)
        check_people_ind4 = np.all(np.array(rec[300:375]) == 0)
        check_people_ind5 = np.all(np.array(rec[375:450]) == 0)

        window0.append(rec[0:75])
        window1.append(rec[75:150])
        window2.append(rec[150:225])
        window3.append(rec[225:300])
        window4.append(rec[300:375])
        window5.append(rec[375:450])
        
        if len(window0) == window0.maxlen:      
            p0 = recognize(window0)
            p1 = recognize(window1)
            p2 = recognize(window2)
            p3 = recognize(window3)
            p4 = recognize(window4)
            p5 = recognize(window5)
        
            result0 = filter0.pre_filer(int(p0[0]))            
            result1 = filter1.pre_filer(int(p1[0]))               
            result2 = filter2.pre_filer(int(p2[0]))                     
            result3 = filter3.pre_filer(int(p3[0]))                
            result4 = filter4.pre_filer(int(p4[0]))                
            result5 = filter5.pre_filer(int(p5[0]))

            if check_people_ind0:
                result0 = 5
            if check_people_ind1:
                result1 = 5
            if check_people_ind2:
                result2 = 5
            if check_people_ind3:
                result3 = 5
            if check_people_ind4:
                result4 = 5
            if check_people_ind5:
                result5 = 5

            actionID1.data = [datasetFileEn[result0], datasetFileEn[result1], datasetFileEn[result2],
                        datasetFileEn[result3], datasetFileEn[result4], datasetFileEn[result5]]
            actionRecognition_pub.publish(actionID1)
            print(actionID1)    
    
        rate.sleep()
        