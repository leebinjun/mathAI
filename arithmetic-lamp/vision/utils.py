import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import cv2
import numpy as np
import config.config as config
import time

# 摄像头畸变矫正 旋转
import json # 使用json存储摄像头矫正参数 
file_name = '.\\config\\config.txt'
with open(file_name) as file_obj:
    temp_d = json.load(file_obj)  # 返回列表数据，也支持字典
mtx = np.array(temp_d['mtx'])   
dist = np.array(temp_d['dist']) 
# print("读取参数: ", mtx， dist)   
def get_camera_img(img):
    img = cv2.undistort(img, mtx, dist, None, mtx)
    img = np.rot90(img)
    return img

# 透射变换
def get_perspective_transform(img_src, points, is_show=False):
    ps_dst = np.float32([[0,0],[0,899],[599, 0],[599,899]])
    ps_src = np.float32(points)
    mat_pers = cv2.getPerspectiveTransform(ps_src, ps_dst)
    img_dst = cv2.warpPerspective(img_src, mat_pers, (600,900))
    if is_show:
        cv2.imshow('rst_image', img_dst)
    return img_dst


# 输入: 投射变换后的试题图片(900,600,3)
# 输出: 第n道算式图片(50,150,3)
def get_equation_n(img, num=0):
    pos_x = 150 * (num // 18)
    pos_y = 50 *  (num % 18)
    img_equation = img[pos_y:pos_y+50, pos_x:pos_x+150, :]
    return img_equation
# 输入: 投射变换后的试题图片(900,600,3)
# 输出: 算式图片的迭代器(50,150,3)
def get_equation(img, num=0):
    while num < 72: #18*4
        pos_x = 150 * (num // 18)
        pos_y = 50 *  (num % 18)
        img_equation = img[pos_y:pos_y+50, pos_x:pos_x+150, :]
        num = num+1
        yield img_equation


SCALSIZE = 1
LARGEST_NUMBER_OF_SYMBOLS = 50
# 读取图片并将图片转化成二值图,返回原彩色图和二值图
def read_img_and_convert_to_binary(img):
    #读取待处理的图片
    original_img = cv2.resize(img, (600,200))
    # print(original_img)
    #将原图分辨率缩小SCALSIZE倍，减少计算复杂度
    original_img = cv2.resize(original_img,(np.int(original_img.shape[1]/SCALSIZE),np.int(original_img.shape[0]/SCALSIZE)), interpolation=cv2.INTER_AREA)
    #降噪
    blur = cv2.GaussianBlur(original_img, (5, 5), 0)
    #将彩色图转化成灰度图
    img_gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    #图片开（opening）处理，用来降噪，使图片中的字符边界更圆滑，没有皱褶
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)

    kernel2 = np.ones((3,3), np.uint8)
    opening = cv2.dilate(opening, kernel2, iterations=1)
    # Otsu's thresholding after Gaussian filtering
    # 采用otsu阈值法将灰度图转化成只有0和1的二值图
    blur = cv2.GaussianBlur(opening,(13,13),0)
    #ret, binary_img = cv2.threshold(img_gray, 120, 1, cv2.THRESH_BINARY_INV)
    ret, binary_img = cv2.threshold(blur,0,1,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return original_img, binary_img

# 输入: 算式图片二值图、算式图片原图
# 输出: [{识别的数字/符号在原图的位置坐标'location':(x,y,w,h),
#        切割的数字/符号图片的保存路径'filepath':r"./data/xxx.jpg"})
def img_segment(binary_img, original_img):
    #寻找每一个字符的轮廓，使用cv2.RETR_EXTERNAL模式，表示只需要每一个字符最外面的轮廓
    img, contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#cv2.RETR_TREE
    #cv2.drawContours(img_original, contours, -1, (0, 255, 0), 2)
    if len(contours) > LARGEST_NUMBER_OF_SYMBOLS:
        raise ValueError('symtem cannot interpret this image!')
    symbol_segment_location = []
    symbol_filepath = []
    # 将每一个联通体，作为一个字符
    index = 1
    # print("len:", len(contours))
    num_id = 0
    for contour in contours:
        location = cv2.boundingRect(contour)
        x, y, w, h = location
        if(w*h<100):
            continue
        # print(f"x, y, w, h: {x},{y},{w},{h}")
        if w > 50: # 两个数字连在一起的情况
            symbol_segment_location.append((x,y,int(w/2),h))
            symbol_segment_location.append((x+w,y,int(w/2),h))
            y_center = int(y + h/2)
            x_center = int(x + w/4)
            img_save = original_img[y_center-32:y_center+32, x_center-21:x_center+21, :]
            num_filepath = r".\data" + '\\' + str(num_id)+'.jpg'
            num_id = num_id + 1
            cv2.imwrite(num_filepath, img_save)
            symbol_filepath.append(num_filepath)
            x_center = int(x + w*3/4)
            img_save = original_img[y_center-32:y_center+32, x_center-21:x_center+21, :]
            num_filepath = r".\data" + '\\' + str(num_id)+'.jpg'
            num_id = num_id + 1
            cv2.imwrite(num_filepath, img_save)
            symbol_filepath.append(num_filepath)
        elif x > 580 or x < 20: # 边缘的噪点
            pass
        else:
            symbol_segment_location.append((x, y, w, h))
            x_center = int(x + w/2)
            y_center = int(y + h/2)
            img_save = original_img[y_center-32:y_center+32, x_center-21:x_center+21, :]
            num_filepath = r".\data" + '\\' + str(num_id)+'.jpg'
            num_id = num_id + 1
            cv2.imwrite(num_filepath, img_save)
            symbol_filepath.append(num_filepath)
        cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        
    symbols = []
    for i in range(len(symbol_segment_location)):
        symbols.append({'location':symbol_segment_location[i], 'filepath':symbol_filepath[i]})
    # 对字符按字符横坐标排序
    symbols.sort(key=lambda x:x['location'][0])
    return symbols


