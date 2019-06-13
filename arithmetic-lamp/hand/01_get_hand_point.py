# Python人体肤色检测 - demo例子集 - 博客园 https://www.cnblogs.com/demodashi/p/9437559.html

import cv2
import numpy as np

# 肤色检测: YCrCb之Cr分量 + OTSU二值化
cap = cv2.VideoCapture(0)
ret, img = cap.read()
while ret:
    ret, img = cap.read()
    
    '''01_肤色检测'''
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb) # 把图像转换到YUV色域
    (y, cr, cb) = cv2.split(ycrcb) # 图像分割, 分别获取y, cr, br通道图像

    # 高斯滤波, cr 是待滤波的源图像数据, (5,5)是值窗口大小, 0 是指根据窗口大小来计算高斯函数标准差
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0) # 对cr通道分量进行高斯滤波
    # 根据OTSU算法求图像阈值, 对图像进行二值化
    _, img_skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 

    # cv2.imshow("image CR", cr1)
    # cv2.imshow("image", img)
    cv2.imshow("Skin Cr+OSTU", img_skin)
    
    k = cv2.waitKey(1)
    if k == ord('s'):
        name = "tmp.jpg"
        cv2.imwrite(name, img)
    if k == ord('q'):
        break
    
    
    '''02_框出手指'''
    # 计算白点数量，过多则认为没有手
    array_a = np.array(img_skin>0)
    # print(array_a.sum())
    if array_a.sum() > 150000:
        continue

    # opencv 3
    image, contours, hierarchy = cv2.findContours(img_skin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
    # opencv 4
    # contours, hierarchy = cv2.findContours(img_skin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
    
    for c in contours:
        if cv2.contourArea(c) > 150000: 
            # print(cv2.contourArea(c))
            break
        elif cv2.contourArea(c) > 2000: 
            (x, y, w, h) = cv2.boundingRect(c)
            # print(f"img_o: {x},{y},{w},{h}")
            img_finger = img_skin[y,x:x+w]
            # print("img_f:", img_finger)
            ret_y = y
            ret_x = x + np.where(img_finger == 255)[0][0]
            # print(f"ret: {ret_x}, {ret_y}")
            cv2.rectangle(img_skin, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.circle(img, (ret_x, ret_y), 10, (0, 255, 255), 5)

    
    cv2.imshow("image", img)
    cv2.imshow("Skin rect", img_skin)

    
    
    


