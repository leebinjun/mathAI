'''
将04_get_num.py得到的数字图片存在r".\data\num\tbd"文件件进行分类
'''
import os
import sys
sys.path.append(".\vision")
from classify_num.classify import Classify
import cv2
import shutil

if __name__ == "__main__":

    ident = Classify()
    path = r".\data\num\tbd"
    img_list = os.listdir(path)
    for filename in img_list:
        img_path = path + '\\' + filename
        ret, score = ident.chessidentify(img_path)
        
        old_path = img_path
        new_path = r'.\data\num' + '\\' + ret + '\\' + filename 
        shutil.copyfile(old_path, new_path)

        print("ret:", ret, score)

