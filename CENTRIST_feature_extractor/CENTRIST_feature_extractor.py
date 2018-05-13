import cv2
import numpy as np
import os
import sys

def censusTransform(image,x,y):
	center=image[x][y]
	neighbours=(image[x-1][y-1],image[x-1][y],image[x-1][y+1],image[x][y-1],image[x][y+1],image[x+1][y-1],image[x+1][y],image[x+1][y+1])
	result=0
	for i in range(8):
		if center>=neighbours[i]:
			result+=2**(7-i)
	return result

def censusTransformHistogram(filename):
	image=cv2.imread(filename,0)
	width,height=image.shape
	width-=2
	height-=2

	ctImage=np.zeros((width,height))
	for i in range(width):
		for j in range(height):
			ctImage[i][j]=censusTransform(image,i+1,j+1)

	hist,_=np.histogram(ctImage.ravel(),254,[1,254])
	return hist

if __name__ == '__main__':
	path=sys.argv[0].split('CENTRIST_feature_extractor.py')[0]
	num=0
	for i in os.listdir(path):
		if i.split('_')[0]=='image':
			num+=1
	result=np.zeros((num,254))
	j=0
	for i in os.listdir(path):
		if i.split('_')[0]=='image':
			result[j,:]=censusTransformHistogram(path+i)
			j+=1
	np.save("CENTRIST_feature.npy",result)