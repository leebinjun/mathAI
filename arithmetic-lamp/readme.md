# 100以内加减法（小学二年级）算数机器人

## 当前的功能
拍一张答题纸，画四个点，透射变换为标准尺寸后进行算式分割，对每张算式图片检测识别数字后进行计算，并打印结果;  
手指指到相应算式下方，语音播报该计算结果。

## 待解决的问题
* 阴影下识别出错  
* 指尖识别只能从一个方向

## 接下来的工作
* GUI
* 写字机器人接入
* 更复杂的算式？

## Demo
![deme](./etcs/000.jpg)
  
![deme](./etcs/001.png)  
  
## 目录
ARITHMETIC-LAMP  
│  1.mp3  
├─ config  
│  │  config.py  
│  └─ config.txt  
├─ data  
│  ├─ calibrate  
│  └─ num  
├─ hand 指尖识别和声音播报  
│  │  01_get_hand_point.py  
│  │  02_test.py  
│  │  03_sound.py  
│  └─ hand_utils.py  
└─ vision 算式识别  
    │  00_cam_test.py  
    │  01_calibrate.py  
    │  02_get_paper.py  
    │  03_get_equation.py  
    │  04_get_num.py  
    │  05_num_classify_test.py  
    │  06_test.py  
    │  classify.py  
    │  utils.py  
    │  vision.md  
    └─ classify_num  
       │  classify.py  
       │  model.py  
       │  predo.py  
       │  readme.md  
       │  read_image.py  
       │  train.py  
       ├─ data  
       └─ model  
              