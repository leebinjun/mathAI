#! /usr/bin/python3
# -*- coding: utf-8 -*- 
from aip import AipSpeech
  
""" 你的 APPID AK SK """  
APP_ID = 'xxxxxxx'
API_KEY = 'xxxxxxx'  
SECRET_KEY = 'xxxxxxx'  
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

s = '13 加 23 = 36'

result  = client.synthesis(s, 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('1.mp3', 'wb') as f:
        f.write(result)

import os
os.system('1.mp3')

