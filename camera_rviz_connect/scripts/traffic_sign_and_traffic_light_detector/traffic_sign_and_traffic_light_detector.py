#!/usr/bin/env python3

"""
Created on Tue Jun 8 2021

@author: Oshada Jayasinghe
"""

import numpy as np
import tensorrt as trt
import torch
import cv2
import rospy
import time
import os

from utils.inference import TRTInference

from torch2trt import torch2trt
from torch2trt import TRTModule

from sensor_msgs.msg import Image as SensorImage
from static_object_detector_stage2.msg import Traffic_signs
from static_object_detector_stage2.msg import Traffic_lights

classifier=torch.load("/home/xavier/traffic_signs_classifier.pth")

model_trt = TRTModule()
model_trt.load_state_dict(torch.load('/home/xavier/detector_ws/src/static_object_detector_stage2/scripts/traffic_sign_and_traffic_light_detector/traffic_sign_and_traffic_light_classifier.pth'))

traffic_signs_publisher = rospy.Publisher('/traffic_sign_detections', Traffic_signs, queue_size = 1)
traffic_lights_publisher = rospy.Publisher('/traffic_light_detections', Traffic_lights, queue_size = 1)

trt_inference_wrapper = TRTInference("/home/xavier/detector_ws/src/static_object_detector_stage2/scripts/traffic_sign_and_traffic_light_detector/traffic_sign_and_traffic_light_detector.buf", trt.DataType.HALF, batch_size=1)

def filter_detections(height, width, detection_out, keep_count_out, min_score_thresh = 0.5):  # filter detections based on the score threshold

    trt_prediction_layout = {"image_id": 0, "label": 1, "score": 2, "xmin": 3, "ymin": 4, "xmax": 5, "ymax": 6}
    prediction_fields = len(trt_prediction_layout)

    detections = {'bboxes': [], 'scores': [], 'classes': []}

    for det in range(int(keep_count_out[0])):

        score = detection_out[det * prediction_fields + trt_prediction_layout["score"]]
        if score < min_score_thresh:
            continue

        class_id = int(detection_out[det * prediction_fields + trt_prediction_layout["label"]])

        x_min = detection_out[det * prediction_fields + trt_prediction_layout["xmin"]]
        y_min = detection_out[det * prediction_fields + trt_prediction_layout["ymin"]]
        x_max = detection_out[det * prediction_fields + trt_prediction_layout["xmax"]]
        y_max = detection_out[det * prediction_fields + trt_prediction_layout["ymax"]]
    
        bbox = (int(x_min * width), int(y_min * height), int(x_max * width), int(y_max * height))
                
        detections['bboxes'].append(bbox)
        detections['scores'].append(score)
        detections['classes'].append(class_id)

    return detections

label_map = {1: 'PRS', 2: 'OSD', 3: 'PHS', 4: 'MNS', 5: 'APR', 6: 'SLS', 7: 'TLS', 8: 'DWS'}

frame_count = 0
total_fps = 0

# warming up GPU
for i in range(10):
    trt_inference_wrapper.infer_img(np.zeros((3,300,300)))

for i in range(10):
    model_trt(torch.rand((1, 3, 100, 100)).cuda())

print("Started Traffic Signs and Traffic Lights Detector")

def detect_traffic_signs(frame, frame_height, frame_width, input_size = (300, 300)):
                                    
    width, height = 1920, 1080
          
    detection_out, keep_count_out = trt_inference_wrapper.infer_img(cv2.resize(frame, input_size))

    detections = filter_detections(height, width, detection_out, keep_count_out, min_score_thresh = 0.5)

    no_of_detections = len(detections['classes'])

    no_of_traffic_signs = 0
    no_of_traffic_lights = 0

    traffic_signs_bboxes = []
    traffic_signs_class_ids = []

    traffic_lights_bboxes = []
    traffic_lights_class_ids = []

    for i in range(no_of_detections): 
        class_id = detections['classes'][i]
        class_name = label_map[class_id]
        x_min, y_min, x_max, y_max =  detections["bboxes"][i]

        sign = frame[y_min:y_max,x_min:x_max]
        sign = cv2.resize(sign,(100, 100)).astype(np.float32)
        sign = torch.from_numpy(sign).cuda()
        sign = sign.permute(2,0,1)/255.0

        if i == 0:
            signs = torch.unsqueeze(sign,0)
        else:
            signs = torch.cat((signs,torch.unsqueeze(sign,0)))

    if no_of_detections!=0:
        out = torch.nn.Softmax(dim = 1)(model_trt(signs))
        class_ids = torch.argmax(out, axis = 1).data.cpu().numpy()

    for i in range(no_of_detections):
        class_id = int(class_ids[i])
        if out[i][class_id]<0.9:  # filtering out detections with low confidence than 0.9
            continue
        x_min, y_min, x_max, y_max =  detections["bboxes"][i]
        bbox = [[x_min, y_min], [x_min, y_max], [x_max, y_max], [x_max, y_min]]
        if class_id >= 70:
            traffic_lights_bboxes.append(bbox)
            traffic_lights_class_ids.append(class_id)
            no_of_traffic_lights += 1
        else:
            traffic_signs_bboxes.append(bbox)
            traffic_signs_class_ids.append(class_id)
            no_of_traffic_signs += 1

    traffic_signs_bboxes = np.array(traffic_signs_bboxes, dtype = np.int32).reshape(-1)
    traffic_lights_bboxes = np.array(traffic_lights_bboxes, dtype = np.int32).reshape(-1)
 
    return no_of_traffic_signs, traffic_signs_bboxes, traffic_signs_class_ids, no_of_traffic_lights, traffic_lights_bboxes, traffic_lights_class_ids 
                        
def callback(data):

    global frame_count, total_fps

    frame_height = data.height
    frame_width = data.width

    frame = np.frombuffer(data.data, dtype = np.uint8).reshape(frame_height, frame_width, -1)
    
    t1 = time.time()

    no_of_traffic_signs, traffic_signs_bboxes, traffic_signs_class_ids, no_of_traffic_lights, traffic_lights_bboxes, traffic_lights_class_ids = detect_traffic_signs(frame, frame_height, frame_width)

    t2 = time.time()

    traffic_signs = Traffic_signs()
    traffic_lights = Traffic_lights()

    traffic_signs.header.stamp = rospy.Time.now()
    traffic_signs.header.seq = data.header.seq
    traffic_signs.frame_height = frame_height
    traffic_signs.frame_width = frame_width
    traffic_signs.inference_time = t2 - t1
    traffic_signs.no_of_traffic_signs = no_of_traffic_signs
    traffic_signs.bounding_boxes = traffic_signs_bboxes
    traffic_signs.class_ids = np.array(traffic_signs_class_ids, dtype = np.int32)

    traffic_lights.header.stamp = rospy.Time.now()
    traffic_lights.header.seq = data.header.seq
    traffic_lights.frame_height = frame_height
    traffic_lights.frame_width = frame_width
    traffic_lights.inference_time = t2 - t1
    traffic_lights.no_of_traffic_lights = no_of_traffic_lights
    traffic_lights.bounding_boxes = traffic_lights_bboxes
    traffic_lights.class_ids = np.array(traffic_lights_class_ids, dtype = np.int32)

    traffic_signs_publisher.publish(traffic_signs)
    traffic_lights_publisher.publish(traffic_lights)

    fps = 1 / (t2 - t1)
    frame_count = frame_count + 1
    total_fps = total_fps + fps

    #print("Traffic Sign & Traffic Light Detection Average FPS :", total_fps / frame_count)

def traffic_sign_and_traffic_light_detector():
    rospy.loginfo("Traffic sign and traffic light detector initiated...")
    rospy.init_node('traffic_sign_and_traffic_light_detector', anonymous = True)
    rospy.Subscriber('/input_frame', SensorImage, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        traffic_sign_and_traffic_light_detector()
    except rospy.ROSInterruptException:
        pass
