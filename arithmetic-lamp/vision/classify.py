from PIL import Image
from matplotlib.pylab import *
import numpy as np
import argparse
import tensorflow as tf
import time
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
 
w = np.int32(42)
h = np.int32(64)
c = np.int32(3)

class Classify():
    
    _instance = None
    classes = ['4','0','9','+','6','-','=','3','5','8','2','7','1']

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Classify, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, model_dir = './vision/classify_num/model/model.ckpt', is_show=False):
        if is_show:
            print("载入模型")
            print("start time:", time.time())
        # Restore model
        self.saver = tf.train.import_meta_graph(model_dir+".meta")
        self.model_dir = model_dir
        if is_show:
            print("end time:", time.time())

    
    def chessidentify(self, filename, is_show = False):
        with tf.Session() as sess:
            self.saver.restore(sess, self.model_dir)
            x = tf.get_default_graph().get_tensor_by_name("images:0")
            keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")
            y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")

            # Read image
            pil_im = array(Image.open(filename), dtype=float32)
            #pil_im = (255-pil_im)/255.0
            pil_im = pil_im.reshape((1,w*h*c))
        
            time1 = time.time()
            # print("pil_im:", pil_im)
            prediction = sess.run(y, feed_dict={x:pil_im,keep_prob: 1.0})
            index = np.argmax(prediction)
            time2 = time.time()
            if is_show:
                print("The classes is: %s. (the probability is %g)" % (self.classes[index], prediction[0][index]))
                
                print("Using time %g" % (time2-time1))

            return self.classes[index], prediction[0][index]




if __name__ == '__main__':
    img_list = [r".\data\num\0\0012.jpg",
                r".\data\num\1\0012.jpg",
                r".\data\num\2\0012.jpg",
                r".\data\num\3\0012.jpg",
                r".\data\num\4\0012.jpg",
                r".\data\num\5\0012.jpg",
                r".\data\num\6\0012.jpg",
                r".\data\num\7\0012.jpg",
                r".\data\num\8\0012.jpg",
                r".\data\num\9\0012.jpg",
                r".\data\num\10\0012.jpg",
                r".\data\num\11\0012.jpg",
                r".\data\num\12\0012.jpg"]
    for img_path in img_list:
        ident = Classify()
        ret, score = ident.chessidentify(img_path)
        print("ret:", ret, score)


    # ident = Classify()
    # for root,dirs,files in os.walk('./vision/classify_chess/data/'):
    #     for file in files:
    #         print(file)
    #         img_path = root+"/"+file
    #         ret, score = ident.chessidentify(img_path)
    #         print("ret:", ret, score)


