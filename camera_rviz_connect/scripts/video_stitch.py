import cv2
import numpy as np
from matplotlib import pyplot as plt

### get the homography matrix
M_str = []
f = open('homography_matrix.txt','r')
for i in range(3):
    M_str.append((f.readline().split()))
f.close()

M = np.array([list(map(float,i)) for i in M_str])

## create masks
narrow_img = cv2.cvtColor(cv2.imread('narrow.png'),cv2.COLOR_BGR2RGB)          # queryImage
wide_img = cv2.cvtColor(cv2.imread('wide.png'),cv2.COLOR_BGR2RGB) # trainImage

h,w,_ = narrow_img.shape
pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
dst = cv2.perspectiveTransform(pts,M)
dst = np.squeeze(dst)


mask = np.zeros([h,w])
cv2.fillPoly(mask,np.int32([dst]),1)
mask_inverse = np.ones([h,w])
cv2.fillPoly(mask_inverse,np.int32([dst]),0)


## read to videos
wide_cap = cv2.VideoCapture('12-11-2021_12-02_camera_0.mp4')
narrow_cap = cv2.VideoCapture('12-11-2021_12-02_camera_1.mp4')

# Check if camera opened successfully
if ((wide_cap.isOpened()== False) or (narrow_cap.isOpened() == False)): 
  print("Error opening video stream or file")

# Read until video is completed

while((wide_cap.isOpened()) and (narrow_cap.isOpened()) ):
  # Capture frame-by-frame
  wide_ret, wide_frame = wide_cap.read()
  narrow_ret, narrow_frame = narrow_cap.read()
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





# warped_narrow_img = cv2.warpPerspective(narrow_img, M, (w, h)) #wraped image
# poly_copied = cv2.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
# img1_middle_removed = cv2.bitwise_and(wide_img,wide_img,mask = np.uint8(mask_inverse))

# concatted_img = np.add(poly_copied,img1_middle_removed)
# plt.imshow(concatted_img,),plt.show()
# # cv2.imwrite("stitched_img.png",cv2.cvtColor(concatted_img,cv2.COLOR_RGB2BGR))