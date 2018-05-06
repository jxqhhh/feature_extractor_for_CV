import cv2
import numpy as np
import os
import sys

# Compute low order moments(1,2,3)
def color_moments(filename):
    img = cv2.imread(filename)
    if img is None:
        return
    # Convert BGR to HSV colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Split the channels - h,s,v
    h, s, v = cv2.split(hsv)
    # Initialize the color feature
    color_feature = np.zeros((1,24))
    # N = h.shape[0] * h.shape[1]
    # The first central moment - average 
    h_mean = np.mean(h)  # np.sum(h)/float(N)
    s_mean = np.mean(s)  # np.sum(s)/float(N)
    v_mean = np.mean(v)  # np.sum(v)/float(N)
    color_feature[0,0:3]=(h_mean,s_mean,v_mean)
    # The second central moment - standard deviation
    h_std = np.std(h)  # np.sqrt(np.mean(abs(h - h.mean())**2))
    s_std = np.std(s)  # np.sqrt(np.mean(abs(s - s.mean())**2))
    v_std = np.std(v)  # np.sqrt(np.mean(abs(v - v.mean())**2))
    color_feature[0,3:6]=(h_std, s_std, v_std)
    # The third central moment - the third root of the skewness
    h_skewness = np.mean(abs(h - h.mean())**3)
    s_skewness = np.mean(abs(s - s.mean())**3)
    v_skewness = np.mean(abs(v - v.mean())**3)
    h_thirdMoment = h_skewness**(1./3)
    s_thirdMoment = s_skewness**(1./3)
    v_thirdMoment = v_skewness**(1./3)
    color_feature[0,6:9]=(h_thirdMoment, s_thirdMoment, v_thirdMoment)
    for i in range(4,9):
    	color_feature[0,3*i-3:3*i]=((np.mean(abs(h - h.mean())**i))**(1./i),(np.mean(abs(s - s.mean())**i))**(1./i),(np.mean(abs(v - v.mean())**i))**(1./i))
    return color_feature

if __name__ == '__main__':
	path=sys.argv[0].split('CM_feature_extractor.py')[0]
	num=0
	for i in os.listdir(path):
		if i.split('_')[-1]=='s.bmp':
			num+=1
	result=np.zeros((num,24))
	j=0
	for i in os.listdir(path):
		if i.split('_')[-1]=='s.bmp':
			feature = color_moments(path+i)
			result[j,:]=feature
			j+=1
	np.save("CM_feature.npy",result)