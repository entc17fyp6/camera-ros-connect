from matplotlib.patches import FancyArrow
import numpy as np

camera_matrix_raw = 15
narrow_cam_details_file = 'narrow_calibration_data\ost.txt'
wide_cam_details_file = 'wide_calibration_data\ost.txt'
wide_traffic_light_file = 'traffic_light_wide_x_y.txt'
narrow_traffic_light_file = 'traffic_light_narrow_x_y.txt'

pixel_width = 2.2*(10^(-6)) ## um
traffic_light_width = 0.2 # m
traffic_light_length = 1 # m

pixel_coords = np.loadtxt(narrow_traffic_light_file, dtype=np.float32, delimiter='\t') # camera matrix
k_narrow = np.loadtxt(narrow_cam_details_file, dtype=np.float32, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ') # camera matrix
k_wide = np.loadtxt(wide_cam_details_file, dtype=np.float32, skiprows=camera_matrix_raw-1, max_rows=3, delimiter=' ') # camera matrix

f_narrow = (k_narrow[0][0] + k_narrow[1][1])/2
f_wide = (k_wide[0][0] + k_wide[1][1])/2

z_vals_narrow = f_narrow*np.array([traffic_light_width, traffic_light_length])/(pixel_width)* 1./(pixel_coords)
print(z_vals_narrow)