# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:11:33 2024

@author: 18705
"""

import cv2
import numpy as np
import time
import pyautogui
from moviepy.editor import ImageSequenceClip
import signal

# 确保已经安装了必要的库
try:
    import cv2
    import numpy as np
    from moviepy.editor import ImageSequenceClip
except ImportError:
    raise Exception("请确保已经安装了cv2, numpy和moviepy库")

# 设置帧率
fps = 10

# 获取屏幕大小
size = (pyautogui.size().width, pyautogui.size().height)

# 初始化一个空列表来存放每一帧图片
frames = []

# 定义信号处理函数，用于捕获Ctrl+C（SIGINT）信号并结束录制
def handle_sigint(signum, frame):
    global running
    running = False
    print("\n已接收到 Ctrl+C，正在结束录制...")
    
running = True
print("开始录制，按'Ctrl+C'结束录制")
signal.signal(signal.SIGINT, handle_sigint)  # 注册信号处理函数

try:
    for i in range(fps * 1000):  # 录制默认设定的10秒，但会根据信号控制实际时长
        if not running:
            break
        
        screen_shot = np.array(pyautogui.screenshot())   # RGB转BGR，适应OpenCV格式
        frames.append(screen_shot)
        time.sleep(1 / fps)

except KeyboardInterrupt:  # 为兼容一些环境下可能直接触发的KeyboardInterrupt异常
    print("\n已通过键盘中断结束录制...")

if frames:  # 如果有至少一帧，则创建视频文件
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile("output.mp4", audio=False)
    print("屏幕录制完成，结果保存在output.mp4文件中")
else:
    print("录制未开始或无有效帧数据，未生成视频文件。")