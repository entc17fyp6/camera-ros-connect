# #! /usr/bin/env python3

# import numpy as np
# import cv2
# import time
# import os
# import rospy
# import threading
# from datetime import datetime
# import subprocess

# width = 1920
# height = 1080
# fps = 30

# # ffmpeg -i input.avi -b:v 64k -bufsize 64k output.avi

# # command = ['ffmpeg',
# #             '-i', '/home/samare/Desktop/outputt.avi',
# #             '-b:v', '64k',
# #             # '-bufsize', '22940k',
# #             '/home/samare/Desktop/new_out.avi'
# # ]

# # p = subprocess.Popen(command, stdin=subprocess.PIPE)

# # subprocess.run(p)

# # command = ['ffmpeg',
# #            '-y', # (optional) overwrite output file if it exists
# #            '-f', 'rawvideo',
# #            '-vcodec', 'rawvideo',
# #             # '-vcodec', 'mpeg',
# #            '-pix_fmt', 'bgr24',
# #            '-s', "{}x{}".format(width, height),
# #            '-r', str(fps),
# #             '-i', '-', # The imput comes from a pipe
# #             '-an', # Tells FFMPEG not to expect any audio
# #            '-c:v', 'libx264',
# #            '-pix_fmt', 'yuv420p',
# #            '-preset', 'ultrafast',
# #            '-f', 'rtp',
           
# #             # '-s', '420x360', # size of one frame
# #             '/home/samare/Desktop/my_output_videofile.avi'
# #            ]

# # q = subprocess.Popen(command, stdin=subprocess.PIPE)

# command = ['ffmpeg',
#             '-i', '/home/samare/Desktop/2.mp4',
#             '-q', '2',
#             '/home/samare/Desktop/1_1111.mp4'
# ]

# r = subprocess.Popen(command, stdin=subprocess.PIPE)
# subprocess.run(r)

#!/usr/bin/env python3

"""
Created on Aug 13 2021
"""
import os
import numpy as np
import cv2
import time
import rospy
import threading

from sensor_msgs.msg import Image as SensorImage

import subprocess
rtmp_url = "rtp://192.168.1.3:1234/stream"
width = 800
height = 450
fps = 30

# command and params for ffmpeg
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'rtp',
           rtmp_url]

# using subprocess and pipe to fetch frame data
p = subprocess.Popen(command, stdin=subprocess.PIPE)

frame_count = 0

frame = None

def output_callback(data):

    global frame, frame_count, _frame, width, height, p

    if frame is not None:

        _frame = cv2.cvtColor(cv2.resize(frame, (800,450)), cv2.COLOR_RGB2BGR)
        p.stdin.write(_frame.tobytes())
        
    frame = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
    frame_count += 1

def streamer():
    rospy.loginfo("Streamer initiated...")
    rospy.init_node('streamer',anonymous=True)
    rospy.Subscriber('/output_frame', SensorImage, output_callback)
    rospy.spin()

if __name__ == '__main__':

    try:
        streamer()
    except rospy.ROSInterruptException:
        pass