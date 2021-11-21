import pypylon.pylon as py
import numpy as np
import matplotlib.pyplot as plt
import traceback
import time
from datetime import datetime
import cv2

import rospy
from sensor_msgs.msg import Image as CameraImage

width = 1080
height = 1920
fps = 30
shold_save_video = False

def publish_image(frame):
    
    frame = draw_time_date(frame)

    input_frame = CameraImage()
    input_frame.header.stamp = rospy.Time.now()
    input_frame.height = frame.shape[0]
    input_frame.width = frame.shape[1]
    input_frame.encoding = "rgb8"
    input_frame.is_bigendian = False
    input_frame.step = 3* frame.shape[1]
    input_frame.data = frame.tobytes()

    input_frame_publisher.publish(input_frame)
    
    if (shold_save_video):
        save_video(frame)

    frame = cv2.cvtColor(cv2.resize(frame, (height,width)), cv2.COLOR_RGB2BGR)
    cv2.namedWindow("Input")
    cv2.imshow("Input", frame)
    cv2.waitKey(1)

    return

def draw_time_date(frame):

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (1150, 50)
    fontScale = 1
    color = (255, 255, 0)
    thickness = 2

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    frame = cv2.putText(frame, dt_string, org, font, fontScale, color, thickness, cv2.LINE_AA)

    return frame

def save_video(frame):
    frame = np.frombuffer(frame, dtype=np.uint8).reshape(width, height, -1)
    # frame = cv2.cvtColor(cv2.resize(frame, (height,width)), cv2.COLOR_RGB2BGR)

    output_video.write(frame)
    return

def initialize_cam(cam):
    cam.UserSetSelector = 'Default'
    cam.UserSetLoad.Execute()

    cam.ExposureAuto = 'Off'
    cam.PixelFormat = 'YCbCr422_8'
    cam.ExposureTime = 30000
    cam.AcquisitionFrameRate = fps

class ImageHandler (py.ImageEventHandler):
    def __init__(self, *args):
        super().__init__(*args)
        self.time_old = time.time()

        self.converter = py.ImageFormatConverter()
        self.converter.OutputPixelFormat = py.PixelType_RGB8packed
        self.converter.OutputBitAlignment = "MsbAligned"
    
    def OnImageGrabbed(self, camera, grabResult):
        try:
            if grabResult.GrabSucceeded():
                
                if (~self.converter.ImageHasDestinationFormat(grabResult)):
                    grabResult = self.converter.Convert(grabResult)
                    
                img = grabResult.Array
                time_new = time.time()
                rate = 1/(time_new-self.time_old)
                print(rate)
                self.time_old = time_new
                publish_image(img)
            else:
                raise RuntimeError("Grab failed")
        except Exception as e:
            traceback.print_exc()

def BackgroundLoop(cam):
    handler = ImageHandler()

    cam.RegisterImageEventHandler(handler, py.RegistrationMode_ReplaceAll, py.Cleanup_None)

    # cam.StartGrabbingMax(100, py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)
    cam.StartGrabbing(py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)

    try:
        while cam.IsGrabbing():
            pass
    except KeyboardInterrupt:
        pass

    cam.StopGrabbing()
    cam.DeregisterImageEventHandler(handler)
    cam.Close()
    cv2.destroyAllWindows()

    # return handler.img_sum


tlf = py.TlFactory.GetInstance()
cam = py.InstantCamera(tlf.CreateFirstDevice())
cam.Open()
initialize_cam(cam)

BackgroundLoop(cam)

def single_camera_grab_image():

    global output_video, input_frame_publisher

    output_video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'MJPG'), fps, (width,height))

    input_frame_publisher = rospy.Publisher('/input_frame',CameraImage,queue_size=1)
    rospy.init_node('image_feeder_node', anonymous=True)

    tlf = py.TlFactory.GetInstance()
    cam = py.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()
    initialize_cam(cam)

    BackgroundLoop(cam)


if __name__ == '__main__':
    try:
        single_camera_grab_image()
    except rospy.ROSInternalException:
        pass