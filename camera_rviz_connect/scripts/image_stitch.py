import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10
narrow_img = cv.imread('narrow_edited.png',0)          # queryImage
wide_img = cv.imread('wide.png',0) # trainImage
# Initiate SIFT detector
sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(narrow_img,None)
kp2, des2 = sift.detectAndCompute(wide_img,None)
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv.FlannBasedMatcher(index_params, search_params)
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
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
    # print(M)
    matchesMask = mask.ravel().tolist()
    h,w = narrow_img.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv.perspectiveTransform(pts,M)
    # wide_img = cv.polylines(wide_img,[np.int32(dst)],True,255,3, cv.LINE_AA)
else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

narrow_img_color = cv.cvtColor(cv.imread('narrow_edited.png'),cv.COLOR_BGR2RGB)          # queryImage
wide_img_color = cv.cvtColor(cv.imread('wide.png'),cv.COLOR_BGR2RGB) # trainImage
# plt.imshow(narrow_img_color), plt.show()
warped_narrow_img = cv.warpPerspective(narrow_img_color, M, ((narrow_img.shape[1]), wide_img.shape[0])) #wraped image

# plt.imshow(dst, 'gray'),plt.show()
dst_2 = np.squeeze(dst)
mask = np.zeros(wide_img.shape)
cv.fillPoly(mask,np.int32([dst_2]),1)
poly_copied = cv.bitwise_and(warped_narrow_img,warped_narrow_img,mask = np.uint8(mask))
# plt.imshow(poly_copied, ),plt.show()

mask_inverse = np.ones(narrow_img.shape)
#assuming src1 and src2 are of same size
cv.fillPoly(mask_inverse,np.int32([dst_2]),0)
img1_middle_removed = cv.bitwise_and(wide_img_color,wide_img_color,mask = np.uint8(mask_inverse))

concatted_img = np.add(poly_copied,img1_middle_removed)
plt.imshow(concatted_img,),plt.show()
