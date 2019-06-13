# a:截取72个算式
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import numpy as np
import cv2
import config.config as config

from utils import get_perspective_transform

points = config.POS

# 600:900
# 4*18
# 150:50
def get_equation(img, num=0):
    while num < 72: #18*4
        pos_x = 150 * (num // 18)
        pos_y = 50 *  (num % 18)
        img_equation = img[pos_y:pos_y+50, pos_x:pos_x+150, :]
        num = num+1
        yield img_equation


def main():

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()

    # 初始化
    import json # 使用json存储摄像头矫正参数 
    file_name = '.\\config\\config.txt'
    with open(file_name) as file_obj:
        temp_d = json.load(file_obj)  # 返回列表数据，也支持字典
    mtx = np.array(temp_d['mtx'])   
    dist = np.array(temp_d['dist']) 
    # print("读取参数：", mtx， dist)   

    img = cv2.undistort(img, mtx, dist, None, mtx)
    img = np.rot90(img)
    img_perspective = get_perspective_transform(img, points)
    
    while ret is True:      
        cv2.namedWindow('image')
        cv2.imshow('image', img_perspective)
        ret, img = cap.read()
        img = cv2.undistort(img, mtx, dist, None, mtx)
        img = np.rot90(img)
        img_perspective = get_perspective_transform(img, points)
        
        ch = cv2.waitKey(5)
        if ch == ord('q') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(r".\data" + '\\' + str(time.time())+'.jpg', img_perspective)
        if ch == ord('a') :
            print("get_equation")
            for img_equation in get_equation(img_perspective):
                cv2.imshow("eq", img_equation)
                cv2.waitKey(0)
                print("here")
                cv2.imwrite(r".\data" + '\\' + str(time.time())+'.jpg', img_equation)

            

if __name__ == '__main__':
    main()