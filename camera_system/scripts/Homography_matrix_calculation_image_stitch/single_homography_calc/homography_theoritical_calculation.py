import numpy as np

camera_matrix_raw = 15
narrow_cam_details_file = 'narrow_calibration_data\ost.txt'
wide_cam_details_file = 'wide_calibration_data\ost.txt'
traffic_light_file = 'traffic_light_narrow_x_y.txt'

pixel_width = 22 ## um

pixel_coords = np.loadtxt(traffic_light_file, dtype=float, delimiter='\t') # camera matrix
k_narrow = np.loadtxt(narrow_cam_details_file, dtype=float, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ') # camera matrix
k_wide = np.loadtxt(wide_cam_details_file, dtype=float, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ') # camera matrix
I = np.eye(3)
t = np.transpose(np.array([[0,0.5,0]]))
n_T =np.array([[0,0,-1]])
print("n_T", n_T.shape, "t", t.shape)
d = 3.5
k_narrow_inv = np.linalg.inv(k_narrow)
middle = I - np.matmul(t,n_T)/d
print("middle", np.matmul(t,n_T))

H_wn = np.matmul(np.matmul(k_wide,middle),k_narrow_inv)

print(H_wn)



# print(pixel_coords.shape)
# print(pixel_coords[1:4])

