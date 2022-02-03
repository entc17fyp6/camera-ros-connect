
from io import RawIOBase
import subprocess as sp
from sys import stderr
import cv2

command = [ "ffmpeg",
            # '-y',
            # '-loglevel', 'error'
            # '-f', 'rawvideo',
            # '-vcodec', 'rawvideo',
            # '-s', '%dx%d' % (1920, 1020),
            # # '-pix_fmt', pixfmt,
            # '-r', '%.02f' % 30,
            # '-i', 'input.mp4',
            # '-f', 'image2pipe',
            # '-pix_fmt', 'rgb24',
            # '-vcodec', "h264_qsv",
            # '-q:v', '30',
            # '-preset', 'fast',
            # '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1'",
            # '-vf', "drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
            # '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1', drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
            # '-vcodec', 'rawvideo', '-an', '-'
        # ]
            # 'ffmpeg',
            '-i', 'input.mp4',
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']
popen_params = {"stdout": sp.PIPE,
                        "stderr": sp.PIPE,
                        "stdin": sp.PIPE,
                        "shell":True   ## keep this line in windows 10, commentout in ubuntu 20.04
                        }
pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT,universal_newlines=True,bufsize=10**8,)
# pipe = sp.Popen(command,bufsize=10**8,  **popen_params)
# self.proc = sp.Popen(cmd, **popen_params)
import numpy
# read 420*360*3 bytes (= 1 frame)
raw_image = pipe.stdout.read(420*360*3)
print("aaa")
print(raw_image)
# transform the byte read into a numpy array
image =  numpy.frombuffer(raw_image, dtype='uint8')
image = image.reshape((360,420,3))
cv2.imshow(image)
cv2.waitKey(0)

# # throw away the data in the pipe's buffer.
# pipe.stdout.flush()
# import ffmpeg
# import numpy as np
# import cv2 
# def extract_frame(input_vid, frame_num):
#     out, _ = (
#         ffmpeg
#         .input(input_vid)
#         .filter_('select', 'gte(n,{})'.format(frame_num))
#         .output('pipe:', format='rawvideo', pix_fmt='bgr24', vframes=1)
#         .run(capture_stdout=True, capture_stderr=True)
#     )
#     return np.frombuffer(out, np.uint8).reshape((1080, 1920, 3))

# for i in range(1):
#     frame = extract_frame('input.mp4',i)
#     # frame = frame.transpose(1,2,0)
#     # frame = np.rollaxis(frame, 0, 0) 
#     # frame = np.rollaxis(frame, 2, 2) 
#     print(frame.shape)
#     cv2.imshow("dd",frame)
#     cv2.waitKey(0)
