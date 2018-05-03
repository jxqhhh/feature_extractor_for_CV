from numpy import *
from numpy import linalg as la
import cv2
import os
import math
import sys

#用最小值作为提取的LBP特征，这样LBP就是旋转不变的了。  
def minBinary(pixel):
	result=255
	for i in range(8):
		tmp=0
		for j in range(8):
			if pixel[(i+j)%8]=='1':
				tmp+=2**j
		if(tmp<result):
			result=tmp
	return result

#加载图像
def loadImageSet(path):
	num=0
	for i in os.listdir(path):
		if i.split('_')[0]=='image':
			num+=1
	FaceMat=mat(zeros((num,928)))
	j=0
	for i in os.listdir(path):
		if i.split('_')[0]=='image':
			try:
				img=cv2.resize(cv2.imread(path+i,0),(29,32))#TODO
			except:
				print('load %s failed'%i)
			FaceMat[j,:]=mat(img).flatten()
			j+=1
	return FaceMat
	'''
	num:图片的数量
	path:图片的存储目录
	'''
def LBP(FaceMat,R=2):
	P=8
	Region8_x=[-1,0,1,1,1,0,-1,-1]
	Region8_y=[-1,-1,-1,0,1,1,1,0]
	pi=math.pi
	LBPoperator=mat(zeros(shape(FaceMat)))
	for i in range(shape(FaceMat)[0]):
		# 对每一个图像进行处理
		tmp=FaceMat[i,:].reshape((29,32))
		H,W=shape(tmp)
		cache=mat(zeros((H,W)))
		for x in range(R,W-R):
			for y in range(R,H-R):
				repixel=''
				pixel=int(tmp[y,x]) 
				for p in range(8): 
					xp = x+Region8_x[p]  
					yp = y+Region8_y[p]  
					if tmp[yp,xp]>pixel:  
						repixel += '1'  
					else:  
						repixel += '0'  
				# minBinary保持LBP算子旋转不变  
				cache[y,x] = minBinary(repixel)
		LBPoperator[i,:] = cache.flatten() 
		# cv2.imwrite(str(i)+'hh.jpg',array(tempface,uint8))  
	return LBPoperator  


if __name__ == '__main__':
	FaceMat=loadImageSet(sys.argv[0].split('LBP_feature_extractor.py')[0])
	LBPoperator=LBP(FaceMat).getA()
	save("LBP_feature.npy",LBPoperator)
