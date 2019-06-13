# 点点，获取试题位置
# 点击顺序： 左上 左下 右上 右下
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import numpy as np
import cv2
import config.config as config

# 43, 13), (42, 620), (428, 11), (430, 619)]
# 600:900
# 4*18
# 150:50
def perTrans(img, points):
    dst = np.float32([[0,0],[0,899],[599, 0],[599,899]])
    src = np.float32(points)
    M = cv2.getPerspectiveTransform(src, dst)
    T = cv2.warpPerspective(img, M, (600,900))
    ROI = np.zeros((900,600,3),np.uint8)
    ROI[:,:] = T
    cv2.imshow('rst_image', ROI)
    # return ROI

global img
global point
points = config.POS
num = 0

def on_mouse(event, x, y, flags, param):
    global img, point, points, num
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point = (x, y)
        points.append(point)
        num += 1
        print(num)
        cv2.circle(img2, point, 10, (0,255,0), 5)
        cv2.imshow('image', img2)
        if num == 4:
            print(points)
            num = 0
            perTrans( img, points)
            
            file_data = ''
            with open(r".\config\config.py", "r", encoding='utf-8') as f:
                for line in f:
                    # print(line)
                    if 'POS = ' in line:
                        new_line = "POS = " + str(points) + '\n'
                        line = new_line
                    file_data += line
            with open(r".\config\config.py", "w", encoding="utf-8") as f:
                f.write(file_data)
                print("ok")
                f.close()
            
            points.clear()

def main():
    global img

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

    perTrans( img, points)
    points.clear()
    while ret is True:
        
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', on_mouse)
        cv2.imshow('image', img)
        ret, img = cap.read()
        img = cv2.undistort(img, mtx, dist, None, mtx)
        img = np.rot90(img)
        
        ch = cv2.waitKey(5)
        if ch == ord('q') :
            break
        # if ch == ord('s') :
        #     print("save photo")
        #     cv2.imwrite(r".\vision" + '\\' + str(time.time())+'.jpg', img)
        #     cv2.imwrite(r".\vision" + '\\' + str(time.time())+'.jpg', img_trans)
        

if __name__ == '__main__':
    main()