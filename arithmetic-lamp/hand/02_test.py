
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import numpy as np
import cv2

from hand.hand_utils import get_hand_points

from hand.hand_utils import client

from vision.utils import get_perspective_transform
from vision.utils import get_camera_img
from vision.utils import get_equation
from vision.utils import get_equation_n
from vision.utils import read_img_and_convert_to_binary
from vision.utils import img_segment

from vision.classify import Classify

import config.config as config
points = config.POS


def main():

    ident = Classify()
    
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    img = get_camera_img(img)
    img_perspective = get_perspective_transform(img, points)
    img_perspective_copy = None
    
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
            img_perspective_copy = img_perspective.copy()
            cv2.imwrite(r".\data" + '\\' + str(time.time())+'.jpg', img_perspective)
        if ch == ord('a'):
            print("get_equation")
            # for id_n in range(1, 72):
            #     img_equation = get_equation_n(img_perspective, num=id_n)
            for img_equation in get_equation(img_perspective):
                cv2.imshow("eq", img_equation)
                # print("here")
                eq_name = r".\data" + '\\' + str(time.time())+'.jpg'
                cv2.imwrite(eq_name, img_equation)
                # cv2.waitKey(0)

                original_img, binary_img = read_img_and_convert_to_binary(img_equation)
                symbols = img_segment(binary_img, original_img)
                cv2.imshow("", original_img)
                # print(symbols)
                cv2.waitKey(0)
                
                s_ret = []
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
            x,y = get_hand_points(img_perspective)
            print("x, y:", x, y)
            if y == 0:
                continue
            n = (x//150)*18 + (y+20)//50

            img_equation = get_equation_n(img_perspective_copy, num=n-1)
            cv2.imshow("eq", img_equation)
            # print("here")
            eq_name = r".\data" + '\\' + str(time.time())+'.jpg'
            cv2.imwrite(eq_name, img_equation)
            # cv2.waitKey(0)

            original_img, binary_img = read_img_and_convert_to_binary(img_equation)
            symbols = img_segment(binary_img, original_img)
            cv2.imshow("", original_img)
            # print(symbols)
            cv2.waitKey(0)

            ans = 0
            s_ret = []
            for i in symbols:
                ret, score = ident.chessidentify(i["filepath"])
                # print("ret:", ret)
                s_ret.append(ret)
            s = "".join(s_ret)
            if len(s_ret) == 5:
                print("no -")
                ans = (ord(s_ret[0]) - ord(s_ret[2]))*10 + (ord(s_ret[1]) - ord(s_ret[3]))
                s = s[:2] + '减' + s[2:]
            else:
                if s_ret[2] == '-':
                    ans = (ord(s_ret[0]) - ord(s_ret[3]))*10 + (ord(s_ret[1]) - ord(s_ret[4]))
                    s = s[:2] + '减' + s[3:]
                elif s_ret[2] == '+':
                    ans = (ord(s_ret[0]) + ord(s_ret[3]))*10 + (ord(s_ret[1]) + ord(s_ret[4])) - 48*2*10 - 48*2
                    s = s[:2] + '加' + s[3:]
                else:
                    print("something wrong!")
            print(s_ret)
            print(ans)

            s = s + str(ans)
            print("s:", s)

            result  = client.synthesis(s, 'zh', 1, {
                'vol': 5,
            })

            # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
            if not isinstance(result, dict):
                with open('1.mp3', 'wb') as f:
                    f.write(result)

            import os
            os.system('1.mp3')

        if ch == ord('c'):
            print("while : get_handfinger_points")
            while ret:
                x_history = []
                y_history = []
                while True:
                    ret, img = cap.read()
                    img = get_camera_img(img)
                    img_perspective = get_perspective_transform(img, points)
                    x,y = get_hand_points(img_perspective)
                    cv2.imshow('image', img_perspective)
                    cv2.waitKey(1)
                    print("x, y:", x, y)
                    if y == 0:
                        continue
                    # x_history.append(x)
                    y_history.append(y)
                    if len(y_history) == 5:
                        # if len(set(y_history)) == 1:
                        print(np.var(np.array(y_history)))
                        if np.var(np.array(y_history)) < 10:
                            break
                        else:
                            y_history = []

                n = (x//150)*18 + (y+20)//50
                img_equation = get_equation_n(img_perspective_copy, num=n-1)
                cv2.imshow("eq", img_equation)
                # print("here")
                eq_name = r".\data" + '\\' + str(time.time())+'.jpg'
                cv2.imwrite(eq_name, img_equation)
                # cv2.waitKey(0)

                original_img, binary_img = read_img_and_convert_to_binary(img_equation)
                symbols = img_segment(binary_img, original_img)
                cv2.imshow("", original_img)
                # print(symbols)
                # cv2.waitKey(0)

                ans = 0
                s_ret = []
                for i in symbols:
                    ret, score = ident.chessidentify(i["filepath"])
                    # print("ret:", ret)
                    s_ret.append(ret)
                s = "".join(s_ret)
                if len(s_ret) == 5:
                    print("no -")
                    ans = (ord(s_ret[0]) - ord(s_ret[2]))*10 + (ord(s_ret[1]) - ord(s_ret[3]))
                    s = s[:2] + '减' + s[2:]
                else:
                    if s_ret[2] == '-':
                        ans = (ord(s_ret[0]) - ord(s_ret[3]))*10 + (ord(s_ret[1]) - ord(s_ret[4]))
                        s = s[:2] + '减' + s[3:]
                    elif s_ret[2] == '+':
                        ans = (ord(s_ret[0]) + ord(s_ret[3]))*10 + (ord(s_ret[1]) + ord(s_ret[4])) - 48*2*10 - 48*2
                        s = s[:2] + '加' + s[3:]
                    else:
                        print("something wrong!")
                print(s_ret)
                print(ans)

                s = s + str(ans)
                print("s:", s)

                result  = client.synthesis(s, 'zh', 1, {
                    'vol': 5,
                })

                # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
                if not isinstance(result, dict):
                    with open('1.mp3', 'wb') as f:
                        f.write(result)

                import os
                os.system('1.mp3')

                cv2.waitKey(100)
                ret, img = cap.read()
                cv2.waitKey(100)
                ret, img = cap.read()

        ret, img = cap.read()


if __name__ == '__main__':
    main()
