import cv2
import time

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open("/home/fyp/Documents/camera-ros-connect/Two_camera_traffic_light/classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

#vc = cv2.VideoCapture("/home/fyp2selfdriving/Documents/traffic_light/yolov4/darknet/video/Colombo_1_1.mp4")
vc = cv2.VideoCapture("/home/fyp/Desktop/test_colombo.mp4")


net = cv2.dnn.readNet("/home/fyp/Documents/camera-ros-connect/Two_camera_traffic_light/weights/yolov4-custom_last.weights", "/home/fyp/Documents/camera-ros-connect/Two_camera_traffic_light/yolov4-custom.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(608, 608), scale=1/255, swapRB=True)

while cv2.waitKey(1) < 1:
    (grabbed, frame) = vc.read()
    if not grabbed:
        exit()

    start = time.time()
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    # print ("classes", classes, '\nscores',scores, '\nboxes',boxes)
    end = time.time()

    start_drawing = time.time()
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        # print("classID",classid)
        print ("class_names", class_names)
        # label = "%s : %f" % (class_names[classid[0]], score)
        label = "%s : %f" % (class_names[int(classid)], score)
        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    end_drawing = time.time()
    
    fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (1 / (end - start), (end_drawing - start_drawing) * 1000)
    cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    fps_label = "FPS: %.2f" % (1 / (end - start))
    print(fps_label)
    cv2.imshow("detections", frame)
    # cv2.waitKey(100)
