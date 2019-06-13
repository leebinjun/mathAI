# a:截取72个算式
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import numpy as np
import cv2

from utils import get_perspective_transform
from utils import get_camera_img
from utils import get_equation
from utils import read_img_and_convert_to_binary
from utils import img_segment

from vision.classify import Classify

import config.config as config
points = config.POS


def main():

    ident = Classify()
    
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    img = get_camera_img(img)
    img_perspective = get_perspective_transform(img, points)
    
    while ret is True:      
        cv2.namedWindow('image')
        cv2.imshow('image', img_perspective)
        ret, img = cap.read()
        img = get_camera_img(img)
        img_perspective = get_perspective_transform(img, points)
        
        ch = cv2.waitKey(5)
        if ch == ord('q'):
            break
        if ch == ord('s'):
            print("save photo")
            cv2.imwrite(r".\data" + '\\' + str(time.time())+'.jpg', img_perspective)
        if ch == ord('a'):
            print("get_equation")
            # for id_n in range(1, 72):
            #     img_equation = get_equation_n(img_perspective, num=id_n)
            for img_equation in get_equation(img_perspective):
                cv2.imshow("eq", img_equation)
                # print("here")
                # eq_name = r".\data" + '\\' + str(time.time())+'.jpg'
                # cv2.imwrite(eq_name, img_equation)
                # cv2.waitKey(0)

                original_img, binary_img = read_img_and_convert_to_binary(img_equation)
                symbols = img_segment(binary_img, original_img)
                cv2.imshow("", original_img)
                # print("syyyyy:", symbols)
                cv2.waitKey(0)
                
                s_ret = []
                ans = 0
                for i in symbols:
                    ret, score = ident.chessidentify(i["filepath"])
                    # print("ret:", ret)
                    s_ret.append(ret)
                if len(s_ret) == 5:
                    print("no -")
                    ans = (ord(s_ret[0]) - ord(s_ret[2]))*10 + (ord(s_ret[1]) - ord(s_ret[3]))
                else:
                    if s_ret[2] == '-':
                        ans = (ord(s_ret[0]) - ord(s_ret[3]))*10 + (ord(s_ret[1]) - ord(s_ret[4]))
                    elif s_ret[2] == '+':
                        ans = (ord(s_ret[0]) + ord(s_ret[3]))*10 + (ord(s_ret[1]) + ord(s_ret[4])) - 48*2*10 - 48*2
                    else:
                        print("something wrong!")
                print(s_ret)
                print(ans)

        if ch == ord('b'):
            print("get_handfinger_points")
            pass
            


if __name__ == '__main__':
    main()
