import pypylon.pylon as py
import numpy as np
import matplotlib.pyplot as plt
import traceback
import time
from datetime import datetime
import cv2
import subprocess as sp
import os

# import rospy
# from sensor_msgs.msg import Image as CameraImage

width = 1080
height = 1920
fps = 10
narrow_AutoExposureTimeUpperLimit = 50000
wide_AutoExposureTimeUpperLimit = 1000
quality_factor = 30
should_feed_video = True
should_visualize = True
apply_filter = False

def image_feed(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV_I420)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BayerBG2BGR)
    return

def visualize(frame):
    # frame= cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.namedWindow("Input")
    cv2.imshow("Input", frame)
    cv2.waitKey(1)
    return

def read_frame(fileloc,frame,fps,num_frame,t_w,t_h) :
    command = ['ffmpeg',
               '-loglevel', 'error',
            #    '-ss', str(datetime.timedelta(seconds=frame/fps)),
               '-i', fileloc,
               #'-vf', '"select=gte(n,%d)"'%(frame),
            #    '-threads', str(1),
            #    '-vf', 'scale=%d:%d'%(t_w,t_h),
               '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1', drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
               '-vframes', str(num_frame),
               '-f', 'image2pipe',
               '-pix_fmt', 'bgr24',
               '-vcodec', 'rawvideo', '-']
    #print(command)
    ffmpeg = sp.Popen(command, stderr=sp.PIPE ,stdout = sp.PIPE )
    out, err = ffmpeg.communicate()
    if(err) :
        print('error',err)
        return None
    img = np.frombuffer(out, np.uint8).reshape((1080, 1920, 3))
    # video = np.fromstring(out, dtype='uint8').reshape((num_frame,t_h,t_w,3)) #NHWC
    return img

def initialize_cam(cam,camera_name):
    cam.UserSetSelector = 'Default'
    cam.UserSetLoad.Execute()

    # cam.PixelFormat = 'YCbCr422_8'
    # cam.ExposureTime = 200
    cam.PixelFormat = 'BayerGB8'
    cam.ExposureTime = 300
    cam.AcquisitionFrameRate = fps
    # cam.BslBrightness = 0.4
    # cam.BslContrast = 0.4
    if (camera_name == 'Narrow'):
        cam.ReverseX = True
        cam.ReverseY = True
        cam.ExposureAuto = 'Continuous'
        cam.AutoExposureTimeUpperLimit = narrow_AutoExposureTimeUpperLimit
        cam.AutoGainUpperLimit = 5.0

        # cam.LightSourcePreset = 'Off'
        # cam.BalanceWhiteAuto = 'Off'
        # cam.Gain = 1
        # cam.GainAuto = 'Off'
        
        # cam.BalanceRatioSelector = 'Red'
        # cam.BalanceRatio = 2.1875
        # cam.BalanceRatioSelector = 'Green'
        # cam.BalanceRatio = 1.46875
        # cam.BalanceRatioSelector = 'Blue'
        # cam.BalanceRatio = 1.76

    if (camera_name == 'Wide'):
        cam.ExposureAuto = 'Continuous'
        cam.AutoExposureTimeUpperLimit = wide_AutoExposureTimeUpperLimit
        cam.AutoGainUpperLimit = 5.0
        

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
                if (should_feed_video):
                    image_feed(img)
                if (should_visualize):
                    visualize(img)
            else:
                raise RuntimeError("Grab failed")
        except Exception as e:
            traceback.print_exc()

def BackgroundLoop(cam):
    handler = ImageHandler()

    cam.RegisterImageEventHandler(handler, py.RegistrationMode_ReplaceAll, py.Cleanup_None)

    global feeder
    # cam.StartGrabbingMax(100, py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)
    cam.StartGrabbing(py.GrabStrategy_LatestImageOnly, py.GrabLoop_ProvidedByInstantCamera)
    # cam.StartGrabbing(py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)

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


################################################
if __name__ == "__main__":
    tlf = py.TlFactory.GetInstance()
    cam = py.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()

    camera_name = cam.DeviceInfo.GetUserDefinedName()
    print(f"connected to {camera_name} camera")

    initialize_cam(cam, camera_name)

    BackgroundLoop(cam)