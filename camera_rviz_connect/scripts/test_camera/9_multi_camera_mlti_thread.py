import pypylon.pylon as py
import numpy as np
import matplotlib.pyplot as plt
import traceback
import time
from datetime import datetime
import cv2
import subprocess as sp
import os

should_save_video = True

width = 1080
height = 1920
fps = 30


tlf = py.TlFactory.GetInstance()
devices = tlf.EnumerateDevices()
cam_count = len(devices)

for d in devices:
    print(d.GetModelName(), d.GetUserDefinedName())

cam_array = []
for i in range (cam_count):
    cam_array.append(py.InstantCamera(tlf.CreateDevice(devices[i])))


for i in range(cam_count):
    cam_array[i].Open()


narrow_cam_id = 0
wide_cam_id = 1
narrow_cam_connected = False
wide_cam_connected = False

for idx, cam in enumerate(cam_array):
    camera_name = cam.DeviceInfo.GetUserDefinedName()
    print(f"set context {idx} for {camera_name} camera")
    if (camera_name == 'Wide'):
        cam.SetCameraContext(wide_cam_id)
        wide_cam_connected = True
    else:
        cam.SetCameraContext(narrow_cam_id)
        narrow_cam_connected = True



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
        cam.AutoExposureTimeUpperLimit = 400
        cam.AutoGainUpperLimit = 5.0
    if (camera_name == 'Wide'):
        cam.ExposureAuto = 'Continuous'
        cam.AutoExposureTimeUpperLimit = 500
        cam.AutoGainUpperLimit = 5.0


for idx, cam in enumerate(cam_array):
    camera_name = cam.DeviceInfo.GetUserDefinedName()
    print(camera_name)
    initialize_cam(cam, camera_name)


class FFMPEG_VideoWriter:
    """ A class for FFMPEG-based video writing.

    A class to write videos using ffmpeg. ffmpeg will write in a large
    choice of formats.

    Parameters
    -----------

    filename
      Any filename like 'video.mp4' etc. but if you want to avoid
      complications it is recommended to use the generic extension
      '.avi' for all your videos.

    size
      Size (width,height) of the output video in pixels.

    fps
      Frames per second in the output video file.

    codec
      FFMPEG codec. It seems that in terms of quality the hierarchy is
      'rawvideo' = 'png' > 'mpeg4' > 'libx264'
      'png' manages the same lossless quality as 'rawvideo' but yields
      smaller files. Type ``ffmpeg -codecs`` in a terminal to get a list
      of accepted codecs.

      Note for default 'libx264': by default the pixel format yuv420p
      is used. If the video dimensions are not both even (e.g. 720x405)
      another pixel format is used, and this can cause problem in some
      video readers.

      Experimentally found best options 
        libx264         - quality - very good     speed - ~30fps achieved       size - 16.74 GB/h
        libx265         - quality - very good     speed - ~15fps achieved       size - 1.396 GB/h
        mjpeg(-q:v=25)  - quality - good          speed - ~30fps achieved       size - 3.66 GB/h
        mpeg(-q:v=11)   - quality - very good     speed - ~30fps achieved       size - 1.624 GB/h
 -
    audiofile
      Optional: The name of an audio file that will be incorporated
      to the video.

    preset
      Sets the time that FFMPEG will take to compress the video. The slower,
      the better the compression rate. Possibilities are: ultrafast,superfast,
      veryfast, faster, fast, medium (default), slow, slower, veryslow,
      placebo. 

      This and affects only for the libx264, libx265 libxvid etc. ('-crf' also affect these types)
      for mjpeg, mpeg4 etc. use -q:v factor

    bitrate
      Only relevant for codecs which accept a bitrate. "5000k" offers
      nice results in general.

    withmask
      Boolean. Set to ``True`` if there is a mask in the video to be
      encoded.

    """

    def __init__(self, filename, size, fps, codec="libx264", audiofile=None,
                 preset="medium", bitrate=None, pixfmt="rgba", quality = '11',crf = '20',
                 logfile=None, threads=None, ffmpeg_params=None):

        if logfile is None:
            logfile = sp.PIPE

        self.filename = filename
        self.codec = codec
        self.ext = self.filename.split(".")[-1]

        # order is important
        cmd = [
            "ffmpeg",
            '-y',
            '-loglevel', 'error' if logfile == sp.PIPE else 'info',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', '%dx%d' % (size[1], size[0]),
            '-pix_fmt', pixfmt,
            '-r', '%.02f' % fps,
            '-i', '-', '-an',
        ]
        cmd.extend([
            '-vcodec', codec,
            '-q:v', quality,
            '-crf', crf,
            '-preset', preset,
        ])
        if ffmpeg_params is not None:
            cmd.extend(ffmpeg_params)
        if bitrate is not None:
            cmd.extend([
                '-b', bitrate
            ])
        if threads is not None:
            cmd.extend(["-threads", str(threads)])

        if ((codec == 'libx264') and
                (size[0] % 2 == 0) and
                (size[1] % 2 == 0)):
            cmd.extend([
                '-pix_fmt', 'yuv420p'
            ])
        cmd.extend([
            filename
        ])

        popen_params = {"stdout": sp.DEVNULL,
                        "stderr": logfile,
                        "stdin": sp.PIPE,
                        "shell":True}

        # This was added so that no extra unwanted window opens on windows
        # when the child process is created
        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000  # CREATE_NO_WINDOW

        self.proc = sp.Popen(cmd, **popen_params)


    def write_frame(self, img_array):
        """ Writes one frame in the file."""
        try:
               self.proc.stdin.write(img_array.tobytes())
        except IOError as err:
            _, ffmpeg_error = self.proc.communicate()
            error = (str(err) + ("\n\nMoviePy error: FFMPEG encountered "
                                 "the following error while writing file %s:"
                                 "\n\n %s" % (self.filename, str(ffmpeg_error))))

            if b"Unknown encoder" in ffmpeg_error:

                error = error+("\n\nThe video export "
                  "failed because FFMPEG didn't find the specified "
                  "codec for video encoding (%s). Please install "
                  "this codec or change the codec when calling "
                  "write_videofile. For instance:\n"
                  "  >>> clip.write_videofile('myvid.webm', codec='libvpx')")%(self.codec)

            elif b"incorrect codec parameters ?" in ffmpeg_error:

                 error = error+("\n\nThe video export "
                  "failed, possibly because the codec specified for "
                  "the video (%s) is not compatible with the given "
                  "extension (%s). Please specify a valid 'codec' "
                  "argument in write_videofile. This would be 'libx264' "
                  "or 'mpeg4' for mp4, 'libtheora' for ogv, 'libvpx for webm. "
                  "Another possible reason is that the audio codec was not "
                  "compatible with the video codec. For instance the video "
                  "extensions 'ogv' and 'webm' only allow 'libvorbis' (default) as a"
                  "video codec."
                  )%(self.codec, self.ext)

            elif  b"encoder setup failed" in ffmpeg_error:

                error = error+("\n\nThe video export "
                  "failed, possibly because the bitrate you specified "
                  "was too high or too low for the video codec.")

            elif b"Invalid encoder type" in ffmpeg_error:

                error = error + ("\n\nThe video export failed because the codec "
                  "or file extension you provided is not a video")


            raise IOError(error)

    def close(self):
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()

        self.proc = None

    # Support the Context Manager protocol, to ensure that resources are cleaned up.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def draw_time_date(frame):

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (1150, 50)
    fontScale = 1
    color = (255, 255, 0)
    thickness = 2

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    frame = cv2.putText(frame, dt_string, org, font, fontScale, color, thickness, cv2.LINE_AA)

    # Attempt to display using cv2 (doesn't work)
    # if (cam_id == 0):
    #     cv2.namedWindow("1")
    #     cv2.imshow("1", frame)
    #     cv2.waitKey(1)
    # else:
    #     cv2.namedWindow("2")
    #     cv2.imshow("2", frame)
    #     cv2.waitKey(1)
        
    return frame


def save_video(frame,cam_id):
    # frame = np.frombuffer(frame, dtype=np.uint8).reshape(width, height, -1)
    # frame = cv2.cvtColor(cv2.resize(frame, (height,width)), cv2.COLOR_RGB2BGR)
    frame = draw_time_date(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV_I420)

    if (should_save_video):
        writer_dict[str(cam_id)].write_frame(frame)
    else:
        cv2.namedWindow(str(cam_id))
        cv2.imshow(str(cam_id), frame)
        cv2.waitKey(1)
    return


converter = py.ImageFormatConverter()
converter.OutputPixelFormat = py.PixelType_RGB8packed
converter.OutputBitAlignment = "MsbAligned"


class ImageHandler (py.ImageEventHandler):
    def __init__(self, *args):
        super().__init__(*args)
        self.time_old = time.time()
        self.time_new = 0
    
    def OnImageGrabbed(self, camera, grabResult):
        try:
            if grabResult.GrabSucceeded():
                
                if (~converter.ImageHasDestinationFormat(grabResult)):
                    grabResult = converter.Convert(grabResult)
                    
                img = grabResult.Array
                cam_id = camera.CameraContext
                self.time_new = time.time()
                rate = 1/(self.time_new-self.time_old)
                if (cam_id == 0):
                    print("                     ",rate,cam_id)
                else:
                    print(rate, cam_id)
                self.time_old = self.time_new
                # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB )
                # cv2.namedWindow("Input")
                # cv2.imshow("Input", img)
                # cv2.waitKey(1)
                save_video(img,cam_id)
            else:
                raise RuntimeError("Grab failed")
        except Exception as e:
            traceback.print_exc()


def BackgroundLoop(cam_array):

    handler_array = []
    for i in range (cam_count):
        handler_array.append(ImageHandler())

    for cam in cam_array:
        cam.RegisterImageEventHandler(handler_array[i], py.RegistrationMode_ReplaceAll, py.Cleanup_None)
        


    # global writer
    # writer = []
    global writer_dict
    writer_dict = {}
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")
    # video_name = dt_string+"_camera_"

    if (wide_cam_connected):
        writer_dict[str(wide_cam_id)] = FFMPEG_VideoWriter("videos/"+dt_string+"_wide_cam"+".mp4",(width, height), fps=fps, pixfmt="yuv420p", codec="h264_qsv", quality='30', preset= 'fast')
    if (narrow_cam_connected):
        writer_dict[str(narrow_cam_id)] = FFMPEG_VideoWriter("videos/"+dt_string+"_narrow_cam"+".mp4",(width, height), fps=fps, pixfmt="yuv420p", codec="h264_qsv", quality='30', preset= 'fast')
    # for i in range(cam_count):
    #     writer.append(FFMPEG_VideoWriter(video_name+str(i)+".mp4",(width, height), fps=fps, pixfmt="yuv420p", codec="h264_qsv", quality='1', preset= 'fast'))
    # writer_1 = FFMPEG_VideoWriter("output_1.mp4",(cam.Height.Value, cam.Width.Value), fps=fps, pixfmt="yuv420p", codec="mpeg4", quality='11', preset= 'ultrafast')
    # writer_2 = FFMPEG_VideoWriter("output_2.mp4",(cam.Height.Value, cam.Width.Value), fps=fps, pixfmt="yuv420p", codec="mpeg4", quality='11', preset= 'ultrafast') 

    # cam.StartGrabbing(py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)
    # cam_array.StartGrabbing(py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)
    for cam in cam_array:
        cam.StartGrabbing(py.GrabStrategy_LatestImages, py.GrabLoop_ProvidedByInstantCamera)

    try:
        while cam_array[0].IsGrabbing():
            pass
    except KeyboardInterrupt:
        pass

    # cam_array.StopGrabbing()
    for i in range (cam_count):
        cam_array[i].StopGrabbing()
        cam_array[i].DeregisterImageEventHandler(handler_array[i])
        # writer[i].close()
    if (wide_cam_connected):
        writer_dict[str(wide_cam_id)].close()
    if (narrow_cam_connected):
        writer_dict[str(narrow_cam_id)].close()
    # cam_array.Close()
    cv2.destroyAllWindows()
    return

BackgroundLoop(cam_array)