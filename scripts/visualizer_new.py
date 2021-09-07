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
from camera_rviz_connect.msg import Road_markings
from camera_rviz_connect.msg import Lanes
from camera_rviz_connect.msg import Traffic_signs
from camera_rviz_connect.msg import Traffic_lights

output_frame_publisher = rospy.Publisher('/output_frame',SensorImage,queue_size=1)

no_of_road_markings = 0
road_marking_polygons = []
road_marking_class_ids = []

no_of_traffic_signs = 0
traffic_sign_bboxes = []
traffic_sign_class_ids = []

no_of_traffic_lights = 0
traffic_light_bboxes = []
traffic_light_class_ids = []

no_of_lanes = 0
lane_coordinates = []

traffic_sign_detection_total_fps = 0
traffic_light_detection_total_fps = 0
road_marking_detection_total_fps = 0
lane_detection_total_fps = 0

traffic_sign_frame_count = 1
traffic_light_frame_count = 1
road_marking_frame_count = 1
lane_frame_count = 1

frame_count = 0

frame = None

road_marking_labels = ["Straight Arrow",
                       "Left Arrow",
                       "Right Arrow",
                       "Straight-Left Arrow",
                       "Straight-Right Arrow",
                       "Junction Box",
                       "Pedestrian Crossing",
                       "Diamond",
                       "Slow",
                       "Bus Lane",
                       "Cycle Lane"]

traffic_sign_and_traffic_light_label_definitions = {
    'APR-09': 'Applicable to All Vehicles', 
    'APR-10': 'Applicable to Light Vehicles', 
    'APR-11': 'Applicable to Heavy Vehicles', 
    'APR-12': 'Applicable to Three Wheels/Tractors', 
    'APR-14': 'Applicable to Unauthorized Vehicles',
    'DWS-01': 'Left Bend Ahead',
    'DWS-02': 'Right Bend Ahead',
    'DWS-03': 'Double Bend to Left',
    'DWS-04': 'Double Bend to Right',
    'DWS-09': 'Road Narrows Ahead',
    'DWS-10': 'Road Narrows on Left',
    'DWS-11': 'Road Narrows on Right',
    'DWS-12': 'Cross Roads Ahead',
    'DWS-13': 'Staggered Junction - First Road Left',
    'DWS-14': 'Staggered Junction - First Road Right',
    'DWS-15': 'T Junction',
    'DWS-16': 'Y Junction',
    'DWS-17': 'Traffic Merges - Left',
    'DWS-18': 'Right Angle Intersection - Left',
    'DWS-19': 'Traffic Merges - Right',
    'DWS-20': 'Right Angle Intersection - Right',
    'DWS-21': 'Narrow Bridge Ahead',
    'DWS-25': 'Roundabout Ahead',
    'DWS-26': 'Light Signals Ahead',
    'DWS-27': 'Dangerous Descent Ahead',
    'DWS-28': 'Dangerous Ascent Ahead',
    'DWS-29': 'Slippery Road Ahead',
    'DWS-32': 'Pedestrian Crossing Ahead',
    'DWS-33': 'Children Crossing Ahead',
    'DWS-35': 'Road Work Ahead',
    'DWS-36': 'Level Crossing with Gates',
    'DWS-40': 'Cyclists Crossing Ahead',
    'DWS-41': 'Animals Crossing Ahead',
    'DWS-42': 'Quay Ahead',
    'DWS-44': 'Road Hump Ahead',
    'DWS-46': 'Dip or Causeway Ahead',
    'MNS-01': 'Turn Left',
    'MNS-02': 'Turn Right',
    'MNS-03': 'Sraight Ahead',
    'MNS-04': 'Turn Left Ahead',
    'MNS-05': 'Turn Right Ahead',
    'MNS-06': 'Pass Left Side',
    'MNS-07': 'Pass Right Side',
    'MNS-09': 'Compulsory Roundabout',
    'OSD-01': 'Pedestrian Crossing',
    'OSD-02': 'One Way Traffic Flow',
    'OSD-03': 'Hospital',
    'OSD-04': 'Parking',
    'OSD-06': 'Bus Stop',
    'OSD-07': 'Bus Lane',
    'OSD-16': 'Entrance to Expressway',
    'OSD-17': 'End of Expressway',
    'OSD-26': 'Exit from Expressway',
    'PHS-01': 'No Entry',
    'PHS-02': 'No Left Turn',
    'PHS-03': 'No Right Turn',
    'PHS-04': 'No U Turn',
    'PHS-09': 'No Horning', 
    'PHS-23': 'No Parking',
    'PHS-24': 'No Parking or Standing',
    'PRS-01': 'Stop',
    'PRS-02': 'Give Way',
    'RSS-02': 'Height Limit',
    'SLS-100': 'Speed Limit - 100',
    'SLS-15': 'Speed Limit - 15',
    'SLS-40': 'Speed Limit - 40',
    'SLS-50': 'Speed Limit - 50',
    'SLS-60': 'Speed Limit - 60',
    'SLS-70': 'Speed Limit - 70',
    'SLS-80': 'Speed Limit - 80',
    'TLS-C': 'Traffic Light - Red and Yellow', 
    'TLS-E': 'Traffic Light - Empty',
    'TLS-G': 'Traffic Light - Green', 
    'TLS-R': 'Traffic Light - Red',
    'TLS-Y': 'Traffic Light - Yellow'}


traffic_sign_and_traffic_light_labels = ['APR-09',
                                         'APR-10', 
                                         'APR-11', 
                                         'APR-12', 
                                         'APR-14', 
                                         'DWS-01', 
                                         'DWS-02', 
                                         'DWS-03', 
                                         'DWS-04', 
                                         'DWS-09', 
                                         'DWS-10', 
                                         'DWS-11', 
                                         'DWS-12', 
                                         'DWS-13', 
                                         'DWS-14', 
                                         'DWS-15', 
                                         'DWS-16', 
                                         'DWS-17', 
                                         'DWS-18', 
                                         'DWS-19', 
                                         'DWS-20', 
                                         'DWS-21', 
                                         'DWS-25', 
                                         'DWS-26', 
                                         'DWS-27', 
                                         'DWS-28', 
                                         'DWS-29', 
                                         'DWS-32', 
                                         'DWS-33', 
                                         'DWS-35', 
                                         'DWS-36', 
                                         'DWS-40', 
                                         'DWS-41', 
                                         'DWS-42', 
                                         'DWS-44', 
                                         'DWS-46', 
                                         'MNS-01', 
                                         'MNS-02', 
                                         'MNS-03', 
                                         'MNS-04', 
                                         'MNS-05', 
                                         'MNS-06', 
                                         'MNS-07', 
                                         'MNS-09', 
                                         'OSD-01', 
                                         'OSD-02', 
                                         'OSD-03', 
                                         'OSD-04', 
                                         'OSD-06', 
                                         'OSD-07', 
                                         'OSD-16', 
                                         'OSD-17', 
                                         'OSD-26', 
                                         'PHS-01', 
                                         'PHS-02', 
                                         'PHS-03', 
                                         'PHS-04', 
                                         'PHS-09', 
                                         'PHS-23', 
                                         'PHS-24', 
                                         'PRS-01', 
                                         'PRS-02', 
                                         'RSS-02', 
                                         'SLS-100', 
                                         'SLS-15', 
                                         'SLS-40', 
                                         'SLS-50', 
                                         'SLS-60', 
                                         'SLS-70', 
                                         'SLS-80', 
                                         'TLS-C', 
                                         'TLS-E', 
                                         'TLS-G', 
                                         'TLS-R', 
                                         'TLS-Y']

traffic_sign_and_traffic_light_labels = [traffic_sign_and_traffic_light_label_definitions[i] for i in traffic_sign_and_traffic_light_labels]

color_map = {"red": (255,0,127),
             "cream": (255,102,178),
             "orange": (255,128,0), 
             "yellow": (255,255,0), 
             "green": (0,255,0), 
             "cyan": (0,255,255), 
             "blue": (0,128,255), 
             "purple": (178,102,255), 
             "pink": (255,0,255)}

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

def draw_traffic_signs(img, no_of_objects, bboxes, class_ids):

    for j in range(no_of_objects):
        points = np.array(bboxes[j*8:j*8 + 8],np.int32).reshape((-1,1,2))
        color = (255,255,255)
        if class_ids[j] >= 0 and class_ids[j] <= 4:  # APR
            color = color_map["orange"]
        if class_ids[j] >= 5 and class_ids[j] <= 35:  # DWS
            color = color_map["yellow"] 
        if class_ids[j] >= 36 and class_ids[j] <= 43:  # MNS
            color = color_map["red"] 
        if class_ids[j] >= 44 and class_ids[j] <= 52:  # OSD
            color = color_map["cyan"] 
        if class_ids[j] >= 53 and class_ids[j] <= 62:  # PHS
            color = color_map["cream"]   
        if class_ids[j] >= 63 and class_ids[j] <= 69:   #SLS
            color = color_map["red"] 
        img = cv2.polylines(img, [points], True, color, thickness = 8)

    for j in range(no_of_objects):
        bbox = bboxes[j*8:j*8 + 8]
        class_name = traffic_sign_and_traffic_light_labels[int(class_ids[j])]
        color = (255,255,255)
        if class_ids[j] >= 0 and class_ids[j] <= 4:  # APR
            color = color_map["orange"]
        if class_ids[j] >= 5 and class_ids[j] <= 35:  # DWS
            color = color_map["yellow"] 
        if class_ids[j] >= 36 and class_ids[j] <= 43:  # MNS
            color = color_map["red"] 
        if class_ids[j] >= 44 and class_ids[j] <= 52:  # OSD
            color = color_map["cyan"] 
        if class_ids[j] >= 53 and class_ids[j] <= 62:  # PHS
            color = color_map["cream"]   
        if class_ids[j] >= 63 and class_ids[j] <= 69:   #SLS
            color = color_map["red"]  
        img = draw_text(img, (bbox[0], bbox[1]), class_name, color)

    return img

def draw_traffic_lights(img, no_of_objects, bboxes, class_ids):

    for j in range(no_of_objects):
        points = np.array(bboxes[j*8:j*8 + 8],np.int32).reshape((-1,1,2))
        color = color_map["purple"] 
        img = cv2.polylines(img, [points], True, color, thickness = 8)

    for j in range(no_of_objects):
        bbox = bboxes[j*8:j*8 + 8]
        class_name = traffic_sign_and_traffic_light_labels[int(class_ids[j])]
        color = color_map["purple"] 
        img = draw_text(img, (bbox[0], bbox[1]), class_name, color)

    return img

def draw_road_markings(img, no_of_objects, polygons, class_ids):

    for j in range(no_of_objects):
        points = np.array(polygons[j*8:j*8 + 8],np.int32).reshape((-1,1,2))
        class_name = road_marking_labels[int(class_ids[j])]
        color = (255,255,255)
        if int(class_ids[j]) < 5:  # SA, RA, LA, SLA, SRA
            color = color_map["pink"] 
        if int(class_ids[j]) in [5,6]:  # PC, JB
            color = color_map["yellow"]  
        if int(class_ids[j]) > 6:  # BL, CL, SL, DM
            color = color_map["red"]              
        img = cv2.polylines(img, [points], True, color, thickness = 8)

    for j in range(no_of_objects):
        polygon = polygons[j*8:j*8 + 8]
        class_name = road_marking_labels[int(class_ids[j])]
        color = (255,255,255)
        if int(class_ids[j]) < 5:  # SA, RA, LA, SLA, SRA
            color = color_map["pink"] 
        if int(class_ids[j]) in [5,6]:  # PC, JB
            color = color_map["yellow"]  
        if int(class_ids[j]) > 6:  # BL, CL, SL, DM
            color = color_map["red"]              
        img = draw_text(img,(polygon[0], polygon[1]), class_name, color)

    return img

def draw_lanes(img, num_lanes, lane_coordinates):

    lane_coordinates = np.reshape(lane_coordinates, (int(len(lane_coordinates) / 4), 4))
 
    for j in range(num_lanes):
        x1, y1, x2, y2 = lane_coordinates[j]
        m = (y2 - y1)/(x2 - x1)
        c = y1 - m*x1
        for y in range(y2, y1, 20):
            x = int((y-c)/m)
            img = cv2.circle(img, (x,y), 8, color_map["green"], -1)
 
    return img

def visualize_FPS_values(img, traffic_sign_detection_average_fps, road_marking_detection_average_fps, lane_detection_average_fps):

    new_img = img.copy()
    font = cv2.FONT_HERSHEY_DUPLEX
    opaque_box = cv2.addWeighted(img[0:130, 0:1050,:], 0.3, np.ones([130,1050,3], dtype = np.uint8) * 0, 0.7, 1.0)
    new_img[0:130, 0:1050,:] = opaque_box
   
    cv2.putText(new_img, 'Traffic Sign and Traffic Light Detection Average FPS : '+str(round(traffic_sign_detection_average_fps,6)), (20,30), font, .9, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(new_img, "Road Markings Detection Average FPS : "+ str(round(road_marking_detection_average_fps,6)), (20,70), font, .9, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(new_img, "Lane Detection Average FPS : "+str(round(lane_detection_average_fps,6)), (20,110), font, .9, (255, 255, 255), 1, cv2.LINE_AA)

    return new_img

def image_callback(data):

    global frame, frame_count

    if frame is not None:
        if no_of_lanes != 0:
            frame = draw_lanes(frame, no_of_lanes, lane_coordinates)
        if no_of_road_markings != 0:
            frame = draw_road_markings(frame, no_of_road_markings, road_marking_polygons, road_marking_class_ids)
        if no_of_traffic_signs != 0:
            frame = draw_traffic_signs(frame, no_of_traffic_signs, traffic_sign_bboxes, traffic_sign_class_ids)
        if no_of_traffic_lights != 0:
            frame = draw_traffic_lights(frame, no_of_traffic_lights, traffic_light_bboxes, traffic_light_class_ids)

        traffic_sign_detection_average_fps = traffic_sign_detection_total_fps / traffic_sign_frame_count
        traffic_light_detection_average_fps = traffic_light_detection_total_fps / traffic_light_frame_count
        road_marking_detection_average_fps = road_marking_detection_total_fps / road_marking_frame_count
        lane_detection_average_fps = lane_detection_total_fps / lane_frame_count
        frame = visualize_FPS_values(frame, traffic_sign_detection_average_fps, road_marking_detection_average_fps, lane_detection_average_fps)
     
        output_frame = SensorImage()
        output_frame.header.stamp = rospy.Time.now()
        output_frame.height = frame.shape[0]
        output_frame.width = frame.shape[1]
        output_frame.encoding = "rgb8"
        output_frame.is_bigendian = False
        output_frame.step = 3 * frame.shape[1]
        output_frame.data = np.array(frame).tobytes()

        output_frame_publisher.publish(output_frame)

        # saving output video if save_output is true
        if rospy.get_param("save_output")==True:
            output_video.write(cv2.cvtColor(cv2.resize(frame, (1920,1080)), cv2.COLOR_RGB2BGR))

    frame = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
    frame_count += 1

def lanes_callback(data):

    global no_of_lanes, lane_coordinates, lane_detection_total_fps, lane_frame_count

    no_of_lanes = data.no_of_lanes
    lane_coordinates = data.lane_coordinates
    lane_detection_total_fps += 1/data.inference_time 
    lane_frame_count += 1

def traffic_signs_callback(data):

    global no_of_traffic_signs, traffic_sign_bboxes, traffic_sign_class_ids, traffic_sign_detection_total_fps, traffic_sign_frame_count

    no_of_traffic_signs = data.no_of_traffic_signs 
    traffic_sign_bboxes = data.bounding_boxes
    traffic_sign_class_ids = data.class_ids
    traffic_sign_detection_total_fps += 1/data.inference_time
    traffic_sign_frame_count += 1

def traffic_lights_callback(data):

    global no_of_traffic_lights, traffic_light_bboxes, traffic_light_class_ids, traffic_light_detection_total_fps, traffic_light_frame_count

    no_of_traffic_lights = data.no_of_traffic_lights 
    traffic_light_bboxes = data.bounding_boxes
    traffic_light_class_ids = data.class_ids
    traffic_light_detection_total_fps += 1/data.inference_time
    traffic_light_frame_count += 1

def road_markings_callback(data):

    global no_of_road_markings, road_marking_polygons, road_marking_class_ids, road_marking_detection_total_fps, road_marking_frame_count

    no_of_road_markings = data.no_of_road_markings
    road_marking_polygons = data.polygons
    road_marking_class_ids = data.class_ids
    road_marking_detection_total_fps += 1/data.inference_time
    road_marking_frame_count += 1

def visualizer_new():
    rospy.loginfo("visualizer_new initiated...")
    rospy.init_node('visualizer_new',anonymous=True)
    rospy.Subscriber('/input_frame',SensorImage, image_callback)
    rospy.Subscriber('/lane_detections',Lanes,lanes_callback)
    rospy.Subscriber('/traffic_sign_detections', Traffic_signs, traffic_signs_callback)
    rospy.Subscriber('/traffic_light_detections',Traffic_lights,traffic_lights_callback)
    rospy.Subscriber('/road_marking_detections', Road_markings, road_markings_callback)
    rospy.Subscriber('/pylon_camera_node/image_raw', SensorImage, image_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        visualizer_new()
    except rospy.ROSInterruptException:
        pass