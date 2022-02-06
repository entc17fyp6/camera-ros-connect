#! /usr/bin/env python3

"""
Created on Tue Jun 8 2021

@author: Oshada Jayasinghe
"""

import numpy as np
import cv2
import time
import rospy

from sensor_msgs.msg import Image as SensorImage
from sensor_msgs.msg import CompressedImage

# output_frame_publisher = rospy.Publisher('/output_frame',SensorImage,queue_size=1)

output_frame_publisher = rospy.Publisher('/compressed_frame', CompressedImage,queue_size=1)

frame_count = 0

frame = None

if rospy.get_param("save_output") == True:
    output_video = cv2.VideoWriter(rospy.get_param("output_video"), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (1920,1080))

def draw_text(img, label_point, text, color):  # for highlighted text

    font_scale = 0.9
    thickness = 5
    text_thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, baseline = cv2.getTextSize(str(text), font, font_scale, thickness)
    text_location = (label_point[0] - 3, label_point[1] + text_size[1] - 41)

    cv2.rectangle(img, (text_location[0] - 2 // 2, text_location[1] - 2 - baseline),
                  (text_location[0] + text_size[0], text_location[1] + text_size[1]), color, -1)
    cv2.putText(img, str(text), (text_location[0], text_location[1] + baseline), font, font_scale, (0, 0, 0), text_thickness, 8)

    return img

def visualize_timeStamp(img, timesStamp_s, timeStamp_ns):

    new_img = img.copy()
    font = cv2.FONT_HERSHEY_DUPLEX
    opaque_box = cv2.addWeighted(img[0:130, 0:1050,:], 0.3, np.ones([130,1050,3], dtype = np.uint8) * 0, 0.7, 1.0)
    new_img[0:130, 0:1050,:] = opaque_box
   
    # cv2.putText(new_img, 'Traffic Sign and Traffic Light Detection Average FPS : '+str(round(traffic_sign_detection_average_fps,6)), (20,30), font, .9, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(new_img, "Road Markings Detection Average FPS : "+ str(round(road_marking_detection_average_fps,6)), (20,70), font, .9, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(new_img, "Lane Detection Average FPS : "+str(round(lane_detection_average_fps,6)), (20,110), font, .9, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(new_img, "Time : "+str(timesStamp_s)+"."+str(timeStamp_ns), (20,110), font, .9, (255, 255, 255), 1, cv2.LINE_AA)
    return new_img

def image_callback(data):

    global frame, frame_count

    if frame is not None:
        timeStamp_s = data.header.stamp.secs
        timeStamp_ns = data.header.stamp.nsecs
        frame = visualize_timeStamp(frame, timeStamp_s, timeStamp_ns)
     
        output_frame = SensorImage()
        output_frame.header.stamp = rospy.Time.now()
        # output_frame.height = frame.shape[0]
        # output_frame.width = frame.shape[1]
        # output_frame.encoding = "rgb8"
        # output_frame.is_bigendian = False
        output_frame.step = 3 * frame.shape[1]
        output_frame.data = np.array(frame).tobytes()

        output_frame_publisher.publish(output_frame)

        # saving output video if save_output is true
        if rospy.get_param("save_output")==True:
            output_video.write(cv2.cvtColor(cv2.resize(frame, (1920,1080)), cv2.COLOR_RGB2BGR))

    frame = np.frombuffer(data.data, dtype=np.uint8).reshape(1920, , -1)
    frame_count += 1


def visualizer_camera_output():
    rospy.loginfo("visualizer_camera_output initiated...")
    rospy.init_node('visualizer_camera_output',anonymous=True)
    # rospy.Subscriber('/input_frame',SensorImage, image_callback)
    rospy.Subscriber('/pylon_camera_node/image_raw/compressed', CompressedImage, image_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        visualizer_camera_output()
    except rospy.ROSInterruptException:
        pass