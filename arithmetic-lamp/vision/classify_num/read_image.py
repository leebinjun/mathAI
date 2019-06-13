from PIL import Image
import numpy as np
from PIL import Image
from pylab import *
import os
import glob
 
 
# 训练时所用输入长、宽和通道大小
w = 42
h = 64
c = 3

# 将标签转换成one-hot矢量
def to_one_hot(label):
    label_one = np.zeros((len(label),np.max(label)+1))
    for i in range(len(label)):
        label_one[i, label[i]]=1
    return label_one
    
# 读入图片并转化成相应的维度
def read_img(path):
    cate   = [path + x for x in os.listdir(path) if os.path.isdir(path + x)]
    imgs   = []
    labels = []
    for idx, folder in enumerate(cate):
        for im in glob.glob(folder + '/*.jpg'):
            print('reading the image: %s' % (im))
            # 读入图片，并缩小到相应维度
            img = array(Image.open(im), dtype=float32)
            imgs.append(img)
            #img = array(img)
            labels.append(idx)
    data,label = np.asarray(imgs, np.float32), to_one_hot(np.asarray(labels, np.int32))
    
    # 将图片随机打乱
    num_example = data.shape[0]
    arr = np.arange(num_example)
    np.random.shuffle(arr)
    data = data[arr]
    label = label[arr]
    # 80%用于训练，20%用于验证
    ratio = 0.8
    s = np.int(num_example * ratio)
    x_train = data[:s]
    y_train = label[:s]
    x_val   = data[s:]
    y_val   = label[s:]
 
    x_train = np.reshape(x_train, [-1, w*h*c])
    x_val = np.reshape(x_val, [-1, w*h*c])
 
    return x_train, y_train, x_val, y_val
 
if __name__=="__main__":
    # path = './data'
    # x_train, y_train, x_val, y_val = read_img(path)
    pass