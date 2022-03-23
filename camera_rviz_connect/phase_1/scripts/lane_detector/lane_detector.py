#!/usr/bin/env python3

"""
Created on Tue Jun 8 2021

@author: Oshada Jayasinghe
"""

import numpy as np
import torchvision.transforms as transforms
import torch
import time
import cv2
import rospy

from scipy.stats import pearsonr

from sensor_msgs.msg import Image as SensorImage
from static_object_detector_stage2.msg import Lanes

from torch2trt import torch2trt
from torch2trt import TRTModule

model_trt = TRTModule()
model_trt.load_state_dict(torch.load('/home/xavier/detector_ws/src/static_object_detector_stage2/scripts/lane_detector/lane_detector.pth'))

no_of_row_anchors = 18

row_anchor_locations = [121, 131, 141, 150, 160, 170, 180, 189, 199, 209, 219, 228, 238, 248, 258, 267, 277, 287]

no_of_gridding_cells = 100

lanes_publisher = rospy.Publisher('/lane_detections',Lanes, queue_size = 1)

frame_count = 0
total_fps = 0

# warming up GPU
for i in range(10):
    model_trt(torch.rand((1, 3, 288, 800)).cuda())

print("Started Lane Detector")

def detect_lanes(frame, frame_height, frame_width):

    t1 = time.time()

    no_of_lanes = 0
    lane_coordinates = []

    frame = frame[450:,:]
    frame = cv2.resize(frame, (800, 288))

    frame = torch.from_numpy(frame).cuda()
    frame = frame.permute(2, 0, 1)/255.0
    frame = transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))(frame)
    frame = torch.reshape(frame,(1, 3, 288, 800))

    out = model_trt(frame).squeeze()
    out = torch.argmax(out,axis=0).to("cpu").numpy()

    out = out[::-1, :]
    out[out == no_of_gridding_cells] = -1
    out = out + 1

    for l in range(4):
        lane = out[:,l]
        x = np.nonzero(lane)[0]             
        lane = lane[lane != 0]
        if len(lane) >= 6:   # filtering based on minimum lane points threshold
            coeff, pvalue = pearsonr(lane,x)
            if abs(coeff) >= 0.95:   # filtering based on the Perason correlation coefficient threshold
                poly = np.poly1d(np.polyfit(x,lane,1))
                y = poly(x)
                y[y < 1] = 1
                y[y > no_of_gridding_cells] = no_of_gridding_cells
                start_lane_point = [int(y[0] * frame_width / no_of_gridding_cells), int((frame_height - 450) * (row_anchor_locations[no_of_row_anchors - 1 - x[0]] / 288)) - 1 + 450]
                end_lane_point = [int(y[-1] * frame_width / no_of_gridding_cells), int((frame_height - 450) * (row_anchor_locations[no_of_row_anchors - 1 - x[-1]] / 288)) - 1 + 450]
                lane_coordinates.extend(start_lane_point)
                lane_coordinates.extend(end_lane_point)
                no_of_lanes += 1
    
    return no_of_lanes, lane_coordinates

def callback(data):

    global frame_count, total_fps
    
    t1 = time.time()
    
    frame_height = data.height
    frame_width = data.width
    
    frame = np.frombuffer(data.data, dtype = np.uint8).reshape(frame_height, frame_width, -1)
    
    no_of_lanes, lane_coordinates = detect_lanes(frame, frame_height, frame_width)
    
    t2 = time.time()

    lanes = Lanes()

    lanes.header.stamp = rospy.Time.now()
    lanes.header.seq = data.header.seq
    lanes.frame_height = frame_height
    lanes.frame_width = frame_width
    lanes.inference_time = t2 - t1
    lanes.no_of_lanes = int(no_of_lanes)
    lanes.lane_coordinates = np.array(lane_coordinates, dtype = np.int32)

    lanes_publisher.publish(lanes)    

    fps = 1 / (t2 - t1)
    frame_count = frame_count + 1
    total_fps = total_fps + fps

    #print("Lane Detection Average FPS :", total_fps / frame_count)

def lane_detector():
    rospy.loginfo("Lane detector initiated...")
    rospy.init_node('lane_detector', anonymous = True)
    rospy.Subscriber('/input_frame', SensorImage, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        lane_detector()
    except rospy.ROSInterruptException:
        pass
