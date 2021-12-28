import cv2
import numpy as np
from matplotlib import pyplot as plt

## read to videos
# wide_cap = cv2.VideoCapture('../videos/wide_cam/12-11-2021 11-38_camera_0.mp4')
# narrow_cap = cv2.VideoCapture('../videos/narrow_cam/12-11-2021_11-38_camera_1.mp4')
wide_cap = cv2.VideoCapture('C:/Users/Samare/Desktop/02-12-2021_16-11_wide_cam.mp4')
narrow_cap = cv2.VideoCapture('C:/Users/Samare/Desktop/02-12-2021_16-11_narrow_cam.mp4')
# wide_cap = cv2.VideoCapture('test_camera/videos/18-11-2021_09-40_wide_cam.mp4')
# narrow_cap = cv2.VideoCapture('test_camera/videos/18-11-2021_09-40_narrow_cam.mp4')

# wide_frame_count = int(wide_cap.get(cv2.CAP_PROP_FRAME_COUNT))
# narrow_frame_count = int(narrow_cap.get(cv2.CAP_PROP_FRAME_COUNT))
# frame_count_difference = wide_frame_count - narrow_frame_count
# frame_skip_no = int(wide_frame_count/frame_count_difference)

# print(wide_frame_count, narrow_frame_count, frame_skip_no)
# Check if camera opened successfully
if ((wide_cap.isOpened()== False) or (narrow_cap.isOpened() == False)): 
  print("Error opening video stream or file")

## read a single frame to calculate homography between cameras
wide_cap.set(0,1000) #read the 1000mS frame
narrow_cap.set(0,1000)

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
    h,w,_ = narrow_frame.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    # wide_frame = cv2.polylines(wide_frame,[np.int32(dst)],True,255,3, cv2.LINE_AA)
else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

f = open('homography_matrix_2.txt','w')
for i in range(3):
    for j in range(3):
        f.write(str(M[i][j])+' ')
    f.write('\n')
# f.write(str(M))
f.close()

h,w,_ = narrow_frame.shape
pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
dst = cv2.perspectiveTransform(pts,M)
dst = np.squeeze(dst)


mask = np.zeros([h,w])
cv2.fillPoly(mask,np.int32([dst]),1)
mask_inverse = np.ones([h,w])
cv2.fillPoly(mask_inverse,np.int32([dst]),0)



## start video from beginning

wide_cap.set(0,0)
narrow_cap.set(0,0)

# frame_count = 0
while((wide_cap.isOpened()) and (narrow_cap.isOpened()) ):
  # Capture frame-by-frame
  wide_ret, wide_frame = wide_cap.read()
  narrow_ret, narrow_frame = narrow_cap.read()

#   frame_count += 1
#   if (frame_count == frame_skip_no):
#       narrow_ret, narrow_frame = narrow_cap.read()
#       frame_count = 0

  if ((wide_ret == True) and (narrow_ret == True)) :

    warped_narrow_img = cv2.warpPerspective(narrow_frame, M, (w, h)) #wraped image
    poly_copied = cv2.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
    img1_middle_removed = cv2.bitwise_and(wide_frame,wide_frame,mask = np.uint8(mask_inverse))

    concatted_img = np.add(poly_copied,img1_middle_removed)
    # Display the resulting frame
    # cv2.imshow('wide_Frame',wide_frame)
    # cv2.imshow('narrow_frame', narrow_frame)
    cv2.imshow('concatenated_frame', concatted_img)

    # Press Q on keyboard to  exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
wide_cap.release()
narrow_cap.release()

# Closes all the frames
cv2.destroyAllWindows()





# warped_narrow_img = cv2.warpPerspective(narrow_frame, M, (w, h)) #wraped image
# poly_copied = cv2.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
# img1_middle_removed = cv2.bitwise_and(wide_frame,wide_frame,mask = np.uint8(mask_inverse))

# concatted_img = np.add(poly_copied,img1_middle_removed)
# plt.imshow(concatted_img,),plt.show()
# # cv2.imwrite("stitched_img.png",cv2.cvtColor(concatted_img,cv2.COLOR_RGB2BGR))