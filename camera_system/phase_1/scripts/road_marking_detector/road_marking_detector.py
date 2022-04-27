#!/usr/bin/env python3

"""
Created on Tue Jun 8 2021

@author: Oshada Jayasinghe
"""

import numpy as np
import tensorrt as trt
import cv2
import rospy
import time
import torch

from utils.inference import TRTInference

from sensor_msgs.msg import Image as SensorImage
from static_object_detector_stage2.msg import Road_markings

classifier=torch.load("/home/xavier/traffic_signs_classifier.pth")

road_markings_publisher = rospy.Publisher('/road_marking_detections', Road_markings, queue_size = 1)

def get_ipt_transform(frame_height, frame_width, scale_factor):   # obatin the inverse perspective transform

    top_left = (int(0.1823 * frame_width / scale_factor), int(0.7176 * frame_height / scale_factor))
    top_right = (int(0.8333 * frame_width / scale_factor), int(0.7176 * frame_height / scale_factor))
    bottom_right = (int(1.4167 * frame_width / scale_factor), int(1 * frame_height / scale_factor))
    bottom_left = (int(-0.3906 * frame_width / scale_factor), int(1 * frame_height / scale_factor))

    src = np.array((top_left, top_right, bottom_right, bottom_left), np.float32) 

    width_bottom = np.sqrt(((bottom_right[0] - bottom_left[0])**2) + ((bottom_right[1] - bottom_left[1])**2))
    width_top = np.sqrt(((top_right[0] - top_left[0])**2) + ((top_right[1] - top_left[1])**2))

    height_right = np.sqrt(((top_right[0] - bottom_right[0])**2) + ((top_right[1] - bottom_right[1])**2))
    height_left = np.sqrt(((top_left[0] - bottom_left[0])**2) + ((top_left[1] - bottom_left[1])**2))

    max_width = max(int(width_bottom), int(width_top))
    max_height = max(int(height_right), int(height_left))

    dst = np.array([[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]], dtype = "float32")

    ipt_transform = cv2.getPerspectiveTransform(src, dst)

    return ipt_transform, max_height, max_width

def polygon_from_bbox(bbox, ipt_transform_inverse, max_height, max_width, scale_factor, input_size):   # convert the bounding box to a 4-sided polygon

    polygon = []

    for point in bbox:
        out_matrix = np.matmul(ipt_transform_inverse, np.array([point[0] * (max_width / input_size[1]), point[1] * (max_height / input_size[0]), 1]).reshape(3,1))
        polygon.append([int(out_matrix[0,0] * scale_factor / out_matrix[2,0]), int(out_matrix[1,0] * scale_factor / out_matrix[2,0])])

    return polygon

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

trt_inference_wrapper = TRTInference("/home/xavier/detector_ws/src/static_object_detector_stage2/scripts/road_marking_detector/road_marking_detector.buf", trt_engine_datatype=trt.DataType.HALF, batch_size=1)

label_map = {0: 'SA', 1: 'LA', 2: 'RA', 3: 'SLA', 4: 'SRA', 5: 'JB', 6: 'PC', 7: 'DM', 8: 'SL', 9: 'BL', 10: 'CL'}
   
frame_count = 0
total_fps = 0

ipt_transform, max_height, max_width = get_ipt_transform(frame_height = 1080, frame_width = 1920, scale_factor = 4)
ipt_transform_inverse = np.linalg.inv(ipt_transform)

# warming up GPU
for i in range(10):
    trt_inference_wrapper.infer_img(np.zeros((3,300,300)))

print("Started Road Markings Detector")

def detect_road_markings(frame, frame_height, frame_width, scale_factor, input_size = (300, 300)):

    frame = cv2.resize(frame,(int(frame_width / scale_factor),int(frame_height / scale_factor)))
    frame = cv2.warpPerspective(frame, ipt_transform, (max_width, max_height))
    frame = cv2.resize(frame, input_size)

    width, height = frame.shape[0], frame.shape[1]

    detection_out, keep_count_out = trt_inference_wrapper.infer_img(frame)

    detections = filter_detections(height, width, detection_out, keep_count_out, min_score_thresh = 0.5)

    no_of_road_markings = len(detections['classes'])

    polygons_array = []
    class_ids_array = []

    for i in range(no_of_road_markings):
        class_id = detections['classes'][i] - 1
        class_name = label_map[class_id]
        x_min, y_min, x_max, y_max  = detections["bboxes"][i]

        bbox = [[x_min, y_min], [x_min, y_max], [x_max, y_max], [x_max, y_min]]
        polygon = polygon_from_bbox(bbox, ipt_transform_inverse, max_height, max_width, scale_factor, input_size)

        polygons_array.append(polygon)
        class_ids_array.append(class_id)

    polygons_array = np.array(polygons_array, dtype = np.int32).reshape(-1)

    return no_of_road_markings, polygons_array, class_ids_array
                  
def callback(data):

    global frame_count, total_fps

    t1 = time.time()

    frame_height = data.height
    frame_width = data.width

    frame = np.frombuffer(data.data, dtype = np.uint8).reshape(frame_height, frame_width, -1)

    no_of_road_markings, polygons_array, class_ids_array = detect_road_markings(frame,  frame_height, frame_width, scale_factor = 4, input_size = (300, 300))

    t2 = time.time()

    road_markings = Road_markings()

    road_markings.header.stamp = rospy.Time.now()
    road_markings.header.seq = data.header.seq
    road_markings.frame_height = frame_height
    road_markings.frame_width = frame_width
    road_markings.no_of_road_markings = no_of_road_markings
    road_markings.polygons = polygons_array
    road_markings.class_ids = np.array(class_ids_array, dtype = np.int32)
    road_markings.inference_time = t2 - t1

    road_markings_publisher.publish(road_markings)

    fps = 1 / (t2 - t1)
    frame_count = frame_count + 1
    total_fps = total_fps + fps

    #print("Road Marking Detection Average FPS :", total_fps / frame_count)

def road_marking_detector():
    rospy.loginfo("Road marking detector initiated...")
    rospy.init_node('road_marking_detector', anonymous = True)
    rospy.Subscriber('/input_frame', SensorImage, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        road_marking_detector()
    except rospy.ROSInterruptException:
        pass
