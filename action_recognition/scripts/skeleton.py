#!/usr/bin/env python
import json
import numpy as np

skeleton = ['AnkleLeft', 'AnkleRight', 'ElbowLeft', 'ElbowRight', 'FootLeft', 'FootRight', 'HandLeft', 'HandRight', 'HandTipLeft',
            'HandTipRight', 'Head', 'HipLeft', 'HipRight', 'KneeLeft', 'KneeRight', 'Neck', 'ShoulderLeft', 'ShoulderRight',
            'SpineBase', 'SpineMid', 'SpineShoulder', 'ThumbLeft', 'ThumbRight', 'WristLeft', 'WristRight']

skpointLen = len(skeleton)  # 25

##################################
class Skeleton:
    def __init__(self, slidingRange, n_clusters,
                 skeletonTarget = None, debugMode=False, referencePoint="SpineBase"):
        self.slidingRange = slidingRange
        self.overallTypeClusterCenter = None
        self.n_clusters = n_clusters
        self.kmeans, self.targetDataIndexs, self.preData = [], [], []
        self.ReferenceIndex = None
        self.debugMode = debugMode
        self.count = 0
        self.clusters_num = 0
        if skeletonTarget is None:
            self.skeletonTarget = skeleton
        else:
            self.skeletonTarget = skeletonTarget
        self.skeletonMask = []
        for s in range(len(skeleton)):
            self.skeletonMask.append(skeleton[s] in self.skeletonTarget)
        for index, targetSk in enumerate(self.skeletonTarget):
            self.targetDataIndexs.append(skeleton.index(targetSk))
            if targetSk == referencePoint:
                self.ReferenceIndex = index
        if self.ReferenceIndex == None:
            raise Exception("skeletonTarget is not found")
    
    ##################################
    def targetDataConvertToReferenceData(self, targetData):
        originArr = targetData.reshape(-1, len(self.targetDataIndexs), 3)
        if np.array_equal(originArr[0, self.ReferenceIndex, :], [0, 0, 0]):
            return np.reshape(originArr, (-1, ))
        originArr = originArr - \
            originArr[:, self.ReferenceIndex:self.ReferenceIndex+1, :]
        return np.reshape(originArr, (-1, ))
    
    ##################################
    ############ training ############
    def getOneCategoryConcatenateSlidingDataWithDir(self, skeletonDirList):    
        TotalSlidingData = None
        for skDir in skeletonDirList:
            if TotalSlidingData is None:
                TotalSlidingData = self.pathToSlidingData(skDir)
                continue
            TotalSlidingData = np.concatenate(
                (TotalSlidingData, self.pathToSlidingData(skDir)), axis=0)
        return TotalSlidingData
       
    def setClustersCenter(self, ClustersCenter):
        self.overallTypeClusterCenter = ClustersCenter
        
    ##################################
    ############ testing ############
    def fullDataConvertToTargetData(self, fullData):
        fullData = np.array(fullData).reshape([-1, skpointLen, 3])
        targetData = fullData[:, np.array(self.skeletonMask), :]
        return targetData.reshape([-1, self.slidingRange * len(self.skeletonTarget) * 3])

    def predictFast_ontime_fnn(self, overallSlidingBlock):
        means = np.ones(len(self.overallTypeClusterCenter)) * -1
        overallSlidingBlock[0] = self.targetDataConvertToReferenceData(overallSlidingBlock[0])
        means = calcDistanceFast(self.overallTypeClusterCenter, overallSlidingBlock[0]) 
        return means
    
##################################
def GetSkeletonWithDir(ClusterCenterDir, skeletonTarget, referencePoint=None):
    targetSkpointLen = len(skeletonTarget)
    clusters = getClusters(ClusterCenterDir)
    n_clusters = clusters.shape[0]
    slidingRange = int((clusters.shape[1]) / (targetSkpointLen*3))
    if referencePoint is not None:
        ske = Skeleton(slidingRange=slidingRange,
                       n_clusters=n_clusters, skeletonTarget=skeletonTarget,
                       referencePoint=referencePoint)
    else:
        ske = Skeleton(slidingRange=slidingRange,
                       n_clusters=n_clusters, skeletonTarget=skeletonTarget)
    ske.clusters_num = n_clusters
    ske.setClustersCenter(clusters)
    return ske

def getClusters(ClusterCenterDir):
    from pathlib import Path
    clusters = []
    allFileList = list(Path(ClusterCenterDir).glob("*.npy"))
    for name in range(len(allFileList)):
        name = str(name)
        fileName = ClusterCenterDir + '/' + name + ".npy"
        clusters.append(np.load(fileName))
    clusters = np.concatenate(clusters)
    return np.array(clusters)

def calcDistanceFast(clusterCenters, x):
        vector = clusterCenters - x
        distances = np.linalg.norm(vector, axis=1)
        return distances