
## 目录

vision 算式识别  
│  00_cam_test.py             打开摄像头   
│  01_calibrate.py            摄像头标定矫正  
│  02_get_paper.py            投射变换得到所有题目   
│  03_get_equation.py         对投射后的图像切割得到单独算式  
│  04_get_num.py              对切割后的算式提取每一个数字和符号  
│  05_num_classify_test.py    得到更多的数据  
│  06_test.py                 测试  
│  classify.py                classify类  
│  utils.py                   函数  
└─ classify_num               分类模型
    ├─ data                   数据  
    └─ model                  模型  

