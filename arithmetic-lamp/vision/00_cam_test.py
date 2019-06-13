import cv2
import time
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480) #宽度 
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640) #高度
ret, img = cam.read()

# 初始化
import json # 使用json存储摄像头矫正参数 
file_name = '.\\config\\config.txt'
with open(file_name) as file_obj:
    temp_d = json.load(file_obj)  # 返回列表数据，也支持字典
mtx = np.array(temp_d['mtx'])   
dist = np.array(temp_d['dist']) 
# print("读取参数：", mtx， dist)    

while ret:
    ret, img = cam.read()
    img = cv2.undistort(img, mtx, dist, None, mtx)
    cv2.imshow("", img)

    k = cv2.waitKey(1)
     
    if k == ord('s'):
        # # calibratesss
        # name = '.\\data\\time' + str(time.time()) + '.jpg'
        name = "tmp.jpg"
        cv2.imwrite(name, img)
    
    if k == ord('q'):
        break
    
