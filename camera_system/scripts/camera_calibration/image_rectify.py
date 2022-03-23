import numpy as np
import cv2 as cv

# cam_details_file = 'cam_details.txt'
# camera_matrix_raw = 19
# distortion_raw = 24
# rectification_raw = 26
# projection_raw = 32

camera = 'wide'

cam_details_file = camera+'_calibration_data\ost.txt'
# cam_details_file = 'cal_'+camera+'_edited.yml'

camera_matrix_raw = 15
distortion_raw = 20
rectification_raw = 23
projection_raw = 27

mtx = np.loadtxt(cam_details_file, dtype=float, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ')
dist = np.loadtxt(cam_details_file, dtype=float, skiprows=distortion_raw-1,max_rows=1, delimiter=' ')

# print(mtx,dist)

w = 1920
h = 1080
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# print(newcameramtx,roi)
orig_img_path = camera+'_ex2'+'.jpg'
orig_img = cv.imread(orig_img_path)
dst = cv.undistort(orig_img, mtx, dist, None, newcameramtx)
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
cv.imshow('calibresult', dst)
cv.waitKey(0)
cv.imwrite(camera+'_rectified_2.jpg',dst)