#! /usr/bin/env python3

from typing import NewType
import numpy as np
import cv2
import time
import rospy
from datetime import datetime

from sensor_msgs.msg import Image as CameraImage

# import subprocess
width = 1080
height = 1920
fps = 30

frame_count = 0
frame = None

# Define the codec and create VideoWriter object
output_video = cv2.VideoWriter("/home/samare/Desktop/outputt.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (1920,1080))


FFMPEG_BIN = "ffmpeg"

def save_with_ffmpeg(fram):


    return

def draw_time_date(frame):

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (1300, 50)
    fontScale = 1
    color = (255, 255, 0)
    thickness = 2

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    frame = cv2.putText(frame, dt_string, org, font, fontScale, color, thickness, cv2.LINE_AA)

    # Attempt to display using cv2 (doesn't work)
    cv2.namedWindow("Input")
    cv2.imshow("Input", frame)
    cv2.waitKey(1)
    return frame

last_time = 0  ## initialize time
def disp_function_call_rate(new_time):
    global last_time
    rate = 1/(new_time - last_time)
    print("rate = ", rate)
    last_time = new_time


def save_video_callback(data):
    disp_function_call_rate(time.time())

    global frame, frame_count, _frame, width, height

    # if frame is not None:

    #     frame = cv2.cvtColor(cv2.resize(frame, (800,450)), cv2.COLOR_RGB2BGR)
        
    frame = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
    frame = cv2.cvtColor(cv2.resize(frame, (height,width)), cv2.COLOR_RGB2BGR)
    
    frame_count += 1

    frame = draw_time_date(frame)
    output_video.write(frame)




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