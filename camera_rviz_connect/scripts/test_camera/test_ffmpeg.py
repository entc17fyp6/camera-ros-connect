# import subprocess , os
import subprocess as sp


# inVid = "input.mp4"
# outVid = "output.mp4"

# cmd = [
#     "ffmpeg",
#     '-y',
#     # '-loglevel', 'error' if logfile == sp.PIPE else 'info',
#     '-f', 'rawvideo',
#     '-vcodec', 'rawvideo',
#     '-s', '%dx%d' % (1920, 1080),
#     '-pix_fmt', 'rgba',
#     '-r', '%.02f' % 30,
#     '-i', '-', '-an',
# ]
# cmd.extend([
#     '-vcodec', "h264_qsv",
#     '-q:v', "30",
#     # '-crf', crf,
#     '-preset', "medium",
# ])

# cmd.extend([
#     "output.mp4"
# ])

# popen_params = {"stdout": sp.DEVNULL,
#                     "stderr": None,
#                     "stdin": sp.PIPE,
#                     "shell":True}
# proc = sp.Popen(cmd, **popen_params)
# proc = subprocess.Popen('ffmpeg -i input.mp4 ' + '''-vf "[in]drawtext=fontsize=20:fontcolor=White:fontfile='/Windows/Fonts/arial.ttf':text='onLine1':x=(w)/2:y=(h)/2, drawtext=fontsize=20:fontcolor=White:fontfile='/Windows/Fonts/arial.ttf':text='onLine2':x=(w)/2:y=((h)/2)+25, drawtext=fontsize=20:fontcolor=White:fontfile='/Windows/Fonts/arial.ttf':text='onLine3':x=(w)/2:y=((h)/2)+50[out]" -y test_out.avi''' + outVid , shell=True, stderr=subprocess.PIPE)
# proc.wait()
# print( proc.stderr.read())
# os.startfile( outVid )
# proc = subprocess.Popen("ffmpeg" + " -i " + inVid + " -vf drawtext=fontfile='C\:\\Windows\\Fonts\\arial.ttf'|text='test' -y " + outVid , shell=True, stderr=subprocess.PIPE)
proc = sp.Popen("ffmpeg -i input.mp4 -vf \"drawtext=text='Test Text':fontcolor=red:fontsize=75:x=1002:y=100:\" output.mp4" , shell=True, stderr=sp.PIPE)
proc.wait()
print( proc.stderr.read())