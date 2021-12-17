# import subprocess , os
import subprocess as sp
from sys import stderr, stdout
import numpy as np
import cv2

# p1 = sp.Popen('ffmpeg -i input.jpg -f image2pipe -pix_fmt bgr24 -vcodec rawvideo -',shell=True , stdout = sp.PIPE, stderr =  sp.PIPE, text=True)

# p1.wait()

# a =p1.stdout.readlines(1)
# print(a)


command = ['ffmpeg',
           '-i', 'test.jpg',
           '-f', 'image2pipe',
           '-pix_fmt', 'bgr24',
           '-vcodec', 'rawvideo', '-an', '-']

p1 = sp.Popen(command, stdout=sp.PIPE, stderr = sp.DEVNULL)

raw_frame = p1.stdout.read(1920*1080*3)
frame = np.frombuffer(raw_frame, np.uint8)
frame = frame.reshape((1080, 1920, 3))


cv2.imshow('image', frame)
cv2.waitKey(0)