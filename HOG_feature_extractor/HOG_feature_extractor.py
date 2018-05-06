from skimage import feature as ft
import numpy as np
import cv2
import os
import sys

if __name__ == '__main__':
	num=0
	for i in os.listdir(sys.argv[0].split('HOG_feature_extractor.py')[0]):
		if i.split('_')[0]=='image':
			num+=1
	result=np.zeros((num,1984))
	path=sys.argv[0].split('HOG_feature_extractor.py')[0]
	j=0
	for i in os.listdir(path):
		if i.split('_')[0]=='image':
#			print(np.array(cv2.imread(path+i,0).shape))
			feature = ft.hog(cv2.resize(cv2.imread(path+i,0),(40,40)),31,(8,8),(2,2)).reshape((1,1984))
			result[j,:]=feature
			j+=1
	np.save("CM_feature_extractor.npy",result)			
