import numpy as np
import matplotlib.pyplot as plt

camera_matrix_raw = 15
narrow_cam_details_file = 'narrow_calibration_data\ost.txt'
wide_cam_details_file = 'wide_calibration_data\ost.txt'

w = 1080
h = 1920

z = 20 # distance of the object
d = 10 # distance of homography plane
t = np.array([0,0.05,0]) # translation between cameras

x,y = 0.5,0.5 # point on the narrow angle camera frame

X = np.array([x,y,1])

n = np.array([0,0,-1])  # normal vector to the plane
n_trans = np.transpose(n)
k_narrow = np.loadtxt(narrow_cam_details_file, dtype=float, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ') # camera matrix
k_wide = np.loadtxt(wide_cam_details_file, dtype=float, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ') # camera matrix
k_narrow_inv = np.linalg.inv(k_narrow) 

coords = []
coords.append(X)
all_errors = []
def get_error_arr(coord):
    X = coord
    errors = []
    for z in range (1,50,1):

        p_d = 1/z + ((n_trans.dot(k_narrow_inv)).dot(X))/d
        e = k_wide.dot(t)
        print("e=",e)
        print('p_d=',p_d)
        error = p_d*e
        errors.append(error[1])
    return errors

for i in coords:
    all_errors.append(get_error_arr(i))

# print('p_d',p_d)
# print('e=',e)
# print('error',error)
# print(all_errors[0])
# print(p_d-1/z)
# print(1/z)
xx = [i for i in range(1,50)]
plt.plot(xx, all_errors[0])
plt.xlabel('distance')
plt.ylabel('error')
plt.show()