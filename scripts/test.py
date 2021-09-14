#! /usr/bin/env python3

from re import sub
import numpy as np
import cv2
import time
import os
import rospy
import threading
from datetime import datetime
import subprocess

from sensor_msgs.msg import Image as CameraImage

width = 1920
height = 1080
fps = 30

command = ['ffmpeg',
           '-y', # (optional) overwrite output file if it exists
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
            # '-vcodec', 'mpeg',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
            '-i', '-', # The imput comes from a pipe
            '-an', # Tells FFMPEG not to expect any audio
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'rtp',
           
            # '-s', '420x360', # size of one frame
            '/home/samare/Desktop/my_output_videofile.avi'
           ]

p = subprocess.Popen(command, stdin=subprocess.PIPE)
subprocess.run(p)

frame_count = 0
frame = None

def save_video_callback(data):
    global frame, frame_count, width, height, p

    if frame is not None:

        _frame = cv2.cvtColor(cv2.resize(frame, (800,450)), cv2.COLOR_RGB2BGR)
        p.stdin.write(_frame.tobytes())
    
    frame = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
    frame_count += 1
    p.stdin.write(frame.tobytes())

    return


def save_camera_output():
    rospy.loginfo("Save camera output started...")
    rospy.init_node("save_camera_output",anonymous=True)
    rospy.Subscriber('/pylon_camera_node/image_raw', CameraImage, save_video_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        save_camera_output()
    except rospy.ROSInterruptException:
        pass


