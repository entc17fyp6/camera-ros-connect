import cv2
import numpy as np
from matplotlib import pyplot as plt

calibrate_from_vid = True
narrow_cam_calibration_time = 1000 ## ms
wide_cam_calibration_time = 1000  ## ms

capture_time = 333700  ## ms

## read to videos

# wide_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos_12_24\\traffic_light\\24-12-2021_06-51_wide_cam.mp4')
# narrow_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos_12_24\\traffic_light\\24-12-2021_06-51_narrow_cam.mp4')
wide_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos\\27-02-2022_10-47_wide_cam.mp4')
narrow_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos\\27-02-2022_10-47_narrow_cam.mp4')
# wide_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos_12_26\\normal\\26-12-2021_09-42_wide_cam.mp4')
# narrow_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos_12_26\\normal\\26-12-2021_09-42_narrow_cam.mp4')
# wide_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos_12_25\\normal\\25-12-2021_08-59_wide_cam.mp4')
# narrow_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos_12_25\\normal\\25-12-2021_08-59_narrow_cam.mp4')
# wide_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos\\29-12-2021_12-41_wide_cam.mp4')
# narrow_cap = cv2.VideoCapture('D:\\ACA\\fyp\\beslar_cameras\\camera-ros-connect\\camera_rviz_connect\\scripts\\test_camera\\videos\\29-12-2021_12-41_narrow_cam.mp4')

narrow_ret, narrow_frame = narrow_cap.read()
h,w,_ = narrow_frame.shape

# Check if camera opened successfully
if ((wide_cap.isOpened()== False) or (narrow_cap.isOpened() == False)): 
  print("Error opening video stream or file")


if (calibrate_from_vid == True):
  
  wide_ret, wide_frame = wide_cap.read()
  narrow_ret, narrow_frame = narrow_cap.read()

  ## read a single frame to calculate homography between cameras
  wide_cap.set(0,wide_cam_calibration_time) #Current position of the video file in milliseconds.
  narrow_cap.set(0,narrow_cam_calibration_time)

  wide_ret, wide_frame = wide_cap.read()
  narrow_ret, narrow_frame = narrow_cap.read()

  ### calculate homography
  MIN_MATCH_COUNT = 10
  # Initiate SIFT detector
  sift = cv2.SIFT_create()
  # find the keypoints and descriptors with SIFT
  kp1, des1 = sift.detectAndCompute(narrow_frame,None)
  kp2, des2 = sift.detectAndCompute(wide_frame,None)
  FLANN_INDEX_KDTREE = 1
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)
  matches = flann.knnMatch(des1,des2,k=2)
  # store all the good matches as per Lowe's ratio test.
  good = []
  for m,n in matches:
      if m.distance < 0.7*n.distance:
          good.append(m)


  #######################
  if len(good)>MIN_MATCH_COUNT:
      src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      # print(M)
      matchesMask = mask.ravel().tolist()
      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
      dst = cv2.perspectiveTransform(pts,M)
      # wide_frame = cv2.polylines(wide_frame,[np.int32(dst)],True,255,3, cv2.LINE_AA)
  else:
      print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
      matchesMask = None

  f = open('homography_matrix_from_vid.txt','w')
  for i in range(3):
      for j in range(3):
          f.write(str(M[i][j])+' ')
      f.write('\n')
  # f.write(str(M))
  f.close()


else: ## use original homograpy matrix
  M = np.loadtxt('homography_matrix.txt', usecols=range(3))

narrow_ret, narrow_frame = narrow_cap.read()
h,w,_ = narrow_frame.shape
pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
dst = cv2.perspectiveTransform(pts,M)
dst = np.squeeze(dst)


mask = np.zeros([h,w])
cv2.fillPoly(mask,np.int32([dst]),1)
mask_inverse = np.ones([h,w])
cv2.fillPoly(mask_inverse,np.int32([dst]),0)



## start video from beginning

wide_cap.set(0,capture_time) #Current position of the video file in milliseconds.
narrow_cap.set(0,capture_time)

# frame_count = 0

wide_ret, wide_frame = wide_cap.read()
narrow_ret, narrow_frame = narrow_cap.read()

cv2.imshow("wide_frame",wide_frame)
cv2.imshow("narrow_frame",narrow_frame)
cv2.waitKey(0)
# narrow_frame = cv2.cvtColor(cv2.imread('test_camera/narrow_frame.jpg'),cv2.COLOR_BGR2RGB)          # queryImage
# wide_frame = cv2.cvtColor(cv2.imread('test_camera/wide_frame.jpg'),cv2.COLOR_BGR2RGB) # trainImage

h,w = narrow_frame.shape[0:2]
pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
dst = cv2.perspectiveTransform(pts,M)
# wide_img = cv.polylines(wide_img,[np.int32(dst)],True,255,3, cv.LINE_AA)

# plt.imshow(narrow_frame), plt.show()
warped_narrow_img = cv2.warpPerspective(narrow_frame, M, ((narrow_frame.shape[1]), wide_frame.shape[0])) #wraped image

# plt.imshow(dst, 'gray'),plt.show()
dst_2 = np.squeeze(dst)
mask = np.zeros(wide_frame.shape[0:2])
print(mask.shape)
cv2.fillPoly(mask,np.int32([dst_2]),1)
poly_copied = cv2.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
# plt.imshow(poly_copied, ),plt.show()

mask_inverse = np.ones(narrow_frame.shape[0:2])
#assuming src1 and src2 are of same size
cv2.fillPoly(mask_inverse,np.int32([dst_2]),0)
img1_middle_removed = cv2.bitwise_and(wide_frame,wide_frame,mask = np.uint8(mask_inverse))

concatted_img = np.add(poly_copied,img1_middle_removed)
concatted_img = cv2.cvtColor(concatted_img,cv2.COLOR_BGR2RGB)
plt.imshow(concatted_img,),plt.show()
cv2.imwrite("stitched_img.png",cv2.cvtColor(concatted_img,cv2.COLOR_RGB2BGR))
cv2.imwrite("narrow.jpg",narrow_frame)
cv2.imwrite("wide.jpg",wide_frame)

# while((wide_cap.isOpened()) and (narrow_cap.isOpened()) ):
#   # Capture frame-by-frame
#   wide_ret, wide_frame = wide_cap.read()
#   narrow_ret, narrow_frame = narrow_cap.read()

# #   frame_count += 1
# #   if (frame_count == frame_skip_no):
# #       narrow_ret, narrow_frame = narrow_cap.read()
# #       frame_count = 0

#   if ((wide_ret == True) and (narrow_ret == True)) :

#     warped_narrow_img = cv2.warpPerspective(narrow_frame, M, (w, h)) #wraped image
#     poly_copied = cv2.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
#     img1_middle_removed = cv2.bitwise_and(wide_frame,wide_frame,mask = np.uint8(mask_inverse))

#     concatted_img = np.add(poly_copied,img1_middle_removed)
#     # Display the resulting frame
#     # cv2.imshow('wide_Frame',wide_frame)
#     # cv2.imshow('narrow_frame', narrow_frame)
#     cv2.imshow('concatenated_frame', concatted_img)

#     # Press Q on keyboard to  exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#       break

#   # Break the loop
#   else: 
#     break

# # When everything done, release the video capture object
# wide_cap.release()
# narrow_cap.release()

# # Closes all the frames
# cv2.destroyAllWindows()





# warped_narrow_img = cv2.warpPerspective(narrow_frame, M, (w, h)) #wraped image
# poly_copied = cv2.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
# img1_middle_removed = cv2.bitwise_and(wide_frame,wide_frame,mask = np.uint8(mask_inverse))

# concatted_img = np.add(poly_copied,img1_middle_removed)
# plt.imshow(concatted_img,),plt.show()
# # cv2.imwrite("stitched_img.png",cv2.cvtColor(concatted_img,cv2.COLOR_RGB2BGR))