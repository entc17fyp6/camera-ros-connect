import cv2
from cv2 import imwrite

wide_video = 'D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos\\27-02-2022_11-52_wide_cam.mp4'
narrow_video = 'D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos\\27-02-2022_11-52_narrow_cam.mp4'

time = 10950 ## milliseconds

wide_cap = cv2.VideoCapture(wide_video)
narrow_cap = cv2.VideoCapture(narrow_video)

wide_cap.set(0,time)
narrow_cap.set(0,time)

ret, wide_frame = wide_cap.read()
ret, narrow_frame = narrow_cap.read()

cv2.imshow("wide",wide_frame)
cv2.imshow("narrow",narrow_frame)
cv2.waitKey(0)

imwrite('narrow_frame.jpg', narrow_frame)
imwrite('wide_frame.jpg', wide_frame)
