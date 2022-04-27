# Camera System

This repository includes all codes related to the camera system which consists of two Basler DaA1920-30uc cameras. 

(The repository is over 100MB due to unused)

## Python3 implementation
- [9_multi_camera_mlti_thread.py](camera_system\scripts\test_camera\9_multi_camera_mlti_thread.py)
- [10_single_camera_grab_image.py](camera_system\scripts\test_camera\10_single_camera_grab_image.py)

These codes can be used for personal laptops preserving maximum speed (30fps) of cameras. But systems like Jetson AGX Xavier, this is not fast enough. (Maximum achievable speed is between 20-30fps).


<p align="left" width="100%">
    <img src="images\camera_system.jpg" width="800">
</p>



## Traffic light detection using Two Camera input

Object detection model: Yolov4

### Real time traffic light detection


<img src="images/traffic_light_detection.gif" width="700" />

### Combining two camera inputs

<p align="left" width="100%">
    <img src="images/image_stitching.png" width="800">
</p>

<img src="images/image_stitching.png" width="700" />

### System architecture

<img src="images/traffic_light_detection.png" width="700" />
