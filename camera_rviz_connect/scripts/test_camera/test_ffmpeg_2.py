import datetime
import subprocess
import numpy as np
import cv2


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
    ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE ,stdout = subprocess.PIPE )
    out, err = ffmpeg.communicate()
    if(err) :
        print('error',err)
        return None
    img = np.frombuffer(out, np.uint8).reshape((1080, 1920, 3))
    # video = np.fromstring(out, dtype='uint8').reshape((num_frame,t_h,t_w,3)) #NHWC
    return img
img = read_frame('input.mp4',frame=1,fps=30,num_frame=1,t_w=1920,t_h=1080)
cv2.imshow("aa",img)
cv2.waitKey(0)