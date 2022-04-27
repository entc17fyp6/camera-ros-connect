from logging import captureWarnings
import subprocess as sp
from sys import stdin, stdout
import cv2
import numpy as np
import time

# command = ['ffmpeg',
#                 '-y', # (optional) overwrite output file if it exists
#                 '-loglevel', 'error',
#                 '-f', 'rawvideo',
#                 '-vcodec', 'rawvideo',
#                 # '-s', '420x360', # size of one frame
#                 # '-pix_fmt', 'bgr24',
#                 '-r', '%.02f' % 30,
#                 '-i', '-', # The imput comes from a pipe
#                 '-an', # Tells FFMPEG not to expect any audio
               
#             #    '-ss', str(datetime.timedelta(seconds=frame/fps)),
#                #'-vf', '"select=gte(n,%d)"'%(frame),
#             #    '-threads', str(1),
#             #    '-vf', 'scale=%d:%d'%(t_w,t_h),
#                '-f', 'image2pipe',
#                '-pix_fmt', 'bgr24',
#                 # '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1'",
#                '-vcodec', 'rawvideo', '-']

# # img_in = cv2.imread('test.jpg')
# img_in = np.zeros((360, 420, 3), dtype=np.uint8)
# with sp.Popen(command, stdin=sp.PIPE,stdout=sp.PIPE) as process:
#     process.stdin.write(img_in.tobytes())
#     process.stdin.close()

#     process.wait()


############################
# command = ['ffmpeg',
#            '-y', # (optional) overwrite output file if it exists
#            '-f', 'rawvideo',
#            '-vcodec','rawvideo',
#            '-s', '420x360', # size of one frame
#            '-pix_fmt', 'rgb24',
#            '-r', '24', # frames per second
#            '-i', '-', # The imput comes from a pipe
#            '-an', # Tells FFMPEG not to expect any audio
#            '-f', 'image2pipe',
#             '-pix_fmt', 'bgr24',
#             '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1'",
#             '-vcodec', 'rawvideo', '-']

# proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

# a = np.zeros((360, 420, 3), dtype=np.uint8)

# proc.stdin.write(a.tobytes())
# # out = proc.communicate(input=a.tobytes())[0]
# proc.stdin.flush()
# out = proc.stdout.read()
# print(out)


# proc.stdin.close()
# proc.stderr.close()
# proc.wait()

#############################

def read_frame(frame_1,frame,fps,num_frame,t_w,t_h) :
    command = ['ffmpeg', '-y',
                '-s', '{}x{}'.format(1920, 1080),
                '-r', str(30),
                '-an',
                '-pix_fmt', 'rgb24',
                '-c:v', 'rawvideo', '-f', 'rawvideo',
                '-i', '-',
                #'-vf', '"select=gte(n,%d)"'%(frame),
                #    '-threads', str(1),
                #    '-vf', 'scale=%d:%d'%(t_w,t_h),
                '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1', drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
                '-vframes', str(num_frame),
                '-f', 'image2pipe',
                '-pix_fmt', 'bgr24',
                '-vcodec', 'rawvideo', '-']
    #print(command)
    ffmpeg = sp.Popen(command, stderr=sp.PIPE ,stdout = sp.PIPE, stdin=sp.PIPE )
    out, err = ffmpeg.communicate(input=frame_1.tobytes())
    # if(err) :
    #     print('error',err)
    #     return None
    img = np.frombuffer(out, np.uint8).reshape((1080, 1920, 3))
    # video = np.fromstring(out, dtype='uint8').reshape((num_frame,t_h,t_w,3)) #NHWC
    return img

# img_in = np.zeros((360, 420, 3), dtype=np.uint8)
img_in = cv2.imread('test.jpg')
img = read_frame(img_in,frame=1,fps=30,num_frame=1,t_w=1920,t_h=1080)
cv2.imshow("aa",img)
cv2.waitKey(0)