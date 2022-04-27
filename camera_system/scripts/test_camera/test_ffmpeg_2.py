import datetime
import subprocess as sp
import numpy as np
import cv2


# def read_frame(fileloc,frame,fps,num_frame,t_w,t_h) :
#     command = ['ffmpeg',
#                '-loglevel', 'error',
#             #    '-ss', str(datetime.timedelta(seconds=frame/fps)),
#                '-i', fileloc,
#                #'-vf', '"select=gte(n,%d)"'%(frame),
#             #    '-threads', str(1),
#             #    '-vf', 'scale=%d:%d'%(t_w,t_h),
#                '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1', drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
#                '-vframes', str(num_frame),
#                '-f', 'image2pipe',
#                '-pix_fmt', 'bgr24',
#                '-vcodec', 'rawvideo', '-']
#     #print(command)
#     ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE ,stdout = subprocess.PIPE )
#     # out = ffmpeg.stdout.read()
#     # err = ffmpeg.stderr.read()
#     # ffmpeg.stdout.close()
#     out, err = ffmpeg.communicate()
#     if(err) :
#         print('error',err)
#         return None
#     img = np.frombuffer(out, np.uint8).reshape((1080, 1920, 3))
#     # video = np.fromstring(out, dtype='uint8').reshape((num_frame,t_h,t_w,3)) #NHWC
#     return img
# img = read_frame('input.mp4',frame=1,fps=30,num_frame=1,t_w=1920,t_h=1080)
# cv2.imshow("aa",img)
# cv2.waitKey(0)

# def read_frame(frame_1,frame,fps,num_frame,t_w,t_h) :
#     command = ['ffmpeg', '-y',
#                 '-s', '{}x{}'.format(1920, 1080),
#                 '-r', str(30),
#                 '-an',
#                 '-pix_fmt', 'rgb24',
#                 '-c:v', 'rawvideo', '-f', 'rawvideo',
#                 '-i', '-',
#                 #'-vf', '"select=gte(n,%d)"'%(frame),
#                 #    '-threads', str(1),
#                 #    '-vf', 'scale=%d:%d'%(t_w,t_h),
#                 '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1', drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
#                 '-vframes', str(num_frame),
#                 '-f', 'image2pipe',
#                 '-pix_fmt', 'bgr24',
#                 '-vcodec', 'rawvideo', '-']
#     #print(command)
#     ffmpeg = sp.Popen(command, stderr=sp.PIPE ,stdout = sp.PIPE, stdin=sp.PIPE )
#     out, err = ffmpeg.communicate(input=frame_1.tobytes())
#     # ffmpeg.stdin.write(frame_1.tobytes())
#     # out = ffmpeg.stdout.read()

#     # if(err) :
#     #     print('error',err)
#     #     return None
#     img = np.frombuffer(out, np.uint8).reshape((1080, 1920, 3))
#     # video = np.fromstring(out, dtype='uint8').reshape((num_frame,t_h,t_w,3)) #NHWC
#     return img

class ffmpeg_filter_class:
    def __init__(self, h=1080,w=1920,fps=30):
        self.w = w
        self.h = h
        self.command = ['ffmpeg', '-y',
                '-s', '{}x{}'.format(h, w),
                '-f', 'rawvideo',
                '-r', '%.02f' % fps,
                '-an',
                '-pix_fmt', 'bgr24',
                '-i', '-',
                '-vf', "curves=r='0/0 0.25/0.4 0.5/0.5 1/1':g='0/0 0.25/0.4 0.5/0.5 1/1':b='0/0 0.25/0.4 0.5/0.5 1/1', drawtext='fontfile=c\:/Windows/Fonts/Calibri.ttf:text=%{localtime}:fontcolor=yellow:fontsize=35:x=1600:y=20:'",
                '-f', 'image2pipe',
                '-pix_fmt', 'bgr24',
                '-vcodec', 'rawvideo', '-']

        
        self.proc = sp.Popen(self.command, stderr=sp.DEVNULL ,stdout = sp.PIPE, stdin=sp.PIPE )

    def filter(self,frame):
        self.proc.stdin.write(frame.tobytes())
        # frame = self.proc.stdout.read()

        # frame, err = self.proc.communicate(input=frame.tobytes())
        frame = np.frombuffer(frame, np.uint8).reshape((self.h, self.w, 3))
        return frame

        # try:
        #     if (self.proc.stdout.closed):
        #         print('closed')
        #     else:
        #         # self.proc.stdin.write(frame.tobytes())
        #         out, err = self.proc.communicate(input=frame.tobytes())
        #     # out = self.proc.stdout.read()
        #     # frame = np.frombuffer(out, np.uint8).reshape((self.w, self.h, 3))
        #     return frame
        # except IOError as err:
        #     _, ffmpeg_error = self.proc.communicate()
        # raise IOError(ffmpeg_error)

    def close(self):
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()

        self.proc = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()



# img_in = np.zeros((360, 420, 3), dtype=np.uint8)
# img_in = cv2.imread('test.jpg')
cap = cv2.VideoCapture('input.mp4')
count = 0
with ffmpeg_filter_class(h=1080,w=1920,fps=30) as ffmpeg_filter:
    while cap.isOpened():
        print(count)
        count +=1
        ret, frame = cap.read()
        img = ffmpeg_filter.filter(frame)
        cv2.imshow("aa",img)
        cv2.waitKey(0)