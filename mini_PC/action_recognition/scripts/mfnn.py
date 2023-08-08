#!/usr/bin/env python3
import numpy as np
import copy
import skeleton
import random
import time
import itertools

input_num = 25
membership_num = 3
output_num = 5
decide_num = 5
min_decide_num = input_num//decide_num
each_decide_num = membership_num**min_decide_num

#######################################
############## Path name ##############
ske_path = "/home/cirlab/catkin_ws/src/action_recognition/scripts/train_modle_mfnn_spinbase"
weight_path = "/home/cirlab/catkin_ws/src/action_recognition/scripts/train_weight_hongwen_mfnn_spinbase1.npy"

#######################################
############ data function ############
def create_rule_index():
    rule = []
    mu_set_index = []
    for i in range(membership_num):
        rule.append(i)   
    for i in range(min_decide_num):
        mu_set_index.append(rule)
    psi = []
    for i in range(min_decide_num):
        repeat_num = membership_num**(min_decide_num-i-1)
        tile_num = membership_num**(min_decide_num-i)
        if repeat_num == 1:
            p = np.tile(mu_set_index[i], (membership_num**min_decide_num)//tile_num)
            p = np.reshape(p, (len(p), 1))
        else:
            p = np.repeat(mu_set_index[i], repeat_num)
            p = np.tile(p, (membership_num**min_decide_num)//tile_num)
            p = np.reshape(p, (len(p), 1)) 
        psi.append(p)
    return psi

#######################################
############ MFNN function ############

def membership_function_layer_gaussian(x):
    x = np.array(x).reshape((min_decide_num, -1))
    mu1 = np.exp(-((x-3.64104064)**2)/(2*2**2))
    mu2 = np.exp(-((x-8.16408967)**2)/(2*2**2))
    mu3 = np.exp(-((x-12.96039512)**2)/(2*2**2))
    mu1_max_index = np.where(x <= 3.64104064)
    mu3_max_index = np.where(x >= 12.96039512)
    mu1[mu1_max_index] = 1
    mu3[mu3_max_index] = 1
    mu = np.concatenate([mu1, mu2, mu3], axis=1)
    return mu           

def rule_layer(mu_set, index):   
    mu0 = mu_set[0]
    mu1 = mu_set[1]
    mu2 = mu_set[2]

    psi0 = mu0[index[0]]
    psi1 = mu1[index[1]]
    psi2 = mu2[index[2]]

    psi = np.concatenate([psi0, psi1, psi2], axis=1)
    psi_answer = np.prod(psi, axis=1)
    
    return psi_answer

def output_layer(psi, w):
    return np.dot(w, psi)

def prediction_mfnn_ontime(data, weight, index):
    
    data1 = [data[0], data[5], data[10], data[15], data[20]]
    data2 = [data[1], data[6], data[11], data[16], data[21]]
    data3 = [data[2], data[7], data[12], data[17], data[22]]
    data4 = [data[3], data[8], data[13], data[18], data[23]]
    data5 = [data[4], data[9], data[14], data[19], data[24]]
    
    mu_sets1 = membership_function_layer_gaussian(data1)
    mu_sets2 = membership_function_layer_gaussian(data2)
    mu_sets3 = membership_function_layer_gaussian(data3)
    mu_sets4 = membership_function_layer_gaussian(data4)
    mu_sets5 = membership_function_layer_gaussian(data5)
    
    psi_sets1 = rule_layer(mu_sets1, index).reshape(each_decide_num, -1)
    psi_sets2 = rule_layer(mu_sets2, index).reshape(each_decide_num, -1)
    psi_sets3 = rule_layer(mu_sets3, index).reshape(each_decide_num, -1)
    psi_sets4 = rule_layer(mu_sets4, index).reshape(each_decide_num, -1)
    psi_sets5 = rule_layer(mu_sets5, index).reshape(each_decide_num, -1)
    
    psi_sets = np.concatenate([psi_sets1, psi_sets2, psi_sets3, psi_sets4, psi_sets5], axis=0)

    answer = output_layer(psi_sets, weight) # (5*1)  
    return answer, psi_sets
 
