# import numpy as np
# import os
# import cv2


# filename = 'video.avi'
# frames_per_second = 30.0
# res = '720p'

# # Set resolution for the video capture
# # Function adapted from https://kirr.co/0l6qmh
# def change_res(cap, width, height):
#     cap.set(3, width)
#     cap.set(4, height)

# # Standard Video Dimensions Sizes
# STD_DIMENSIONS =  {
#     "480p": (640, 480),
#     "720p": (1280, 720),
#     "1080p": (1920, 1080),
#     "4k": (3840, 2160),
# }


# # grab resolution dimensions and set video capture to it.
# def get_dims(cap, res='1080p'):
#     width, height = STD_DIMENSIONS["480p"]
#     if res in STD_DIMENSIONS:
#         width,height = STD_DIMENSIONS[res]
#     ## change the current caputre device
#     ## to the resulting resolution
#     change_res(cap, width, height)
#     return width, height

# # Video Encoding, might require additional installs
# # Types of Codes: http://www.fourcc.org/codecs.php
# VIDEO_TYPE = {
#     'avi': cv2.VideoWriter_fourcc(*'XVID'),
#     #'mp4': cv2.VideoWriter_fourcc(*'H264'),
#     'mp4': cv2.VideoWriter_fourcc(*'XVID'),
# }

# def get_video_type(filename):
#     filename, ext = os.path.splitext(filename)
#     if ext in VIDEO_TYPE:
#       return  VIDEO_TYPE[ext]
#     return VIDEO_TYPE['avi']



# cap = cv2.VideoCapture(0)
# out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

# while True:
#     ret, frame = cap.read()
#     out.write(frame)
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cap.release()
# out.release()
# cv2.destroyAllWindows()

import os
import pypylon
from imageio import get_writer

while True:
    try:
        fsamp = float(input('Sampling rate (Hz): '))
        break
    except ValueError:
        print('Invalid input.')

time_exposure = 1000000 / fsamp

available_cameras = pypylon.factory.find_devices()
cam = pypylon.factory.create_device(available_cameras[0])
cam.open()

cam.properties['ExposureTime'] = time_exposure

buffer = tuple(cam.grab_images(2000))
with get_writer(
       'I:/output-filename.mkv',  # mkv players often support H.264
        fps=fsamp,  # FPS is in units Hz; should be real-time.
        codec='libx264',  # When used properly, this is basically
                          # "PNG for video" (i.e. lossless)
        quality=None,  # disables variable compression
        pixelformat='rgb24',  # keep it as RGB colours
        ffmpeg_params=[  # compatibility with older library versions
            '-preset',  # set to faster, veryfast, superfast, ultrafast
            'fast',     # for higher speed but worse compression
            '-crf',  # quality; set to 0 for lossless, but keep in mind
            '11'     # that the camera probably adds static anyway
        ]
) as writer:
    for image in buffer:
        writer.append_data(image)
del buffer