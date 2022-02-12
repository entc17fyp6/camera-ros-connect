import cv2
import time
print (cv2.__version__)


vc = cv2.VideoCapture("/home/fyp/Desktop/test_colombo.mp4")


while cv2.waitKey(1) < 1:
    (grabbed, frame) = vc.read()
    if not grabbed:
        exit()

    start = time.time()
    end = time.time()

    start_drawing = time.time()
    end_drawing = time.time()
    
    fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (1 / (end - start), (end_drawing - start_drawing) * 1000)
    cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # fps_label = "FPS: %.2f" % (1 / (end - start))
    print(fps_label)
    cv2.imshow("detections", frame)
    cv2.waitKey(30)


