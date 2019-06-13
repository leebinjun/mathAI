#coding:utf-8
import cv2
import numpy as np

import sys
sys.path.append(".\vision")

#棋盘格模板规格
w = 9
h = 7

class Calibrate (object):
    
    def __init__ (self):
        # 找棋盘格角点
        # 阈值
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        # 世界坐标系中的棋盘格点,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
        self.objp = np.zeros((w*h,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
        # 储存棋盘格角点的世界坐标和图像坐标对
        self.objpoints = [] # 在世界坐标系中的三维点
        self.imgpoints = [] # 在图像平面的二维点
        self.image_shape = [] # 图像大小

        self.calibrate_mtx = []  # 标定用参数
        self.calibrate_dist = []


    def read_sample (self, image_path):
        import glob
        images = glob.glob(image_path)
        for fname in images:
            print(f"{fname}")
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.image_shape = gray.shape

            # 找到棋盘格角点
            ret, corners = cv2.findChessboardCorners(gray, (w,h),None)
            # 如果找到足够点对，将其存储起来
            if ret == True:
                cv2.cornerSubPix(gray,corners,(11,11),(-1,-1), self.criteria)
                self.objpoints.append(self.objp)
                self.imgpoints.append(corners)
                # 将角点在图像上显示
                cv2.drawChessboardCorners(img, (w,h), corners, ret)
                cv2.imshow('findCorners',img)
                cv2.waitKey(1)
        cv2.destroyAllWindows()

    def calibrate(self):
        # 标定
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera( self.objpoints, self.imgpoints, self.image_shape[::-1], None, None)
        '''
        mtx   - 摄像机内矩阵
        dist  - 进一步扭曲
        rvecs - 旋转向量
        tvecs - 平移向量
        '''
        self.calibrate_mtx = mtx
        self.calibrate_dist = dist
        print("mtx:", self.calibrate_mtx)
        print("dist:", self.calibrate_dist)


    # TODO
    def save_parameter(self, filename):
        import pickle
        fw = open(filename,'wb')
        pickle.dump(self.calibrate_dist, fw)
        pickle.dump(self.calibrate_mtx, fw)
        fw.close()

    def load_parameter(self, filename):
        import pickle
        fr = open(filename, 'rb')
        temp = pickle.load(fr)
        print(temp)

    def test(self, image_path):
        # 去畸变
        # image_path = r'.\\Data\\origin\\gobang_chessboard_2.jpg'
        img2 = cv2.imread(image_path)
        
        h, w = img2.shape[:2]
        # undistort
        dst = cv2.undistort(img2, self.calibrate_mtx, self.calibrate_dist, None, self.calibrate_mtx)
        cv2.imwrite('.\\data\\calibresult.png',dst)

        cv2.imshow('img', img2)
        cv2.imshow('dst', dst)
        # wait a 'c'
        while 1:
            ch = cv2.waitKey(1)
            if ch == ord('c') :
                break

    def calculate_error(self):
    # TODO(binjun): 这一部分待完成
        # 反投影误差
        total_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            total_error += error
        print("total error: ", total_error/len(objpoints))


if __name__ == '__main__':
    
    a_temp = Calibrate()

    image_path = '.\\data\\*.jpg'
    a_temp.read_sample(image_path)
    a_temp.calibrate()

    # filename = '.\\Config\\calibrate_config.txt'
    # a_temp.save_parameter(filename)

    # filename = '.\\Config\\calibrate_config.txt'
    # a_temp.load_parameter(filename)

    # # 初始化
    # import json # 使用json存储摄像头矫正参数 
    # file_name = '.\\Config\\config.txt'
    # with open(file_name) as file_obj:
    #     temp_d = json.load(file_obj)  # 返回列表数据，也支持字典
    # mtx = np.array(temp_d['mtx'])   
    # dist = np.array(temp_d['dist']) 
    # print("读取参数：", mtx, dist)    

    # test
    image_path = r'.\data\time1560131719.978197.jpg'
    a_temp.test(image_path)
    




























