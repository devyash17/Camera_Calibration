# MapmyIndia Internship Plan
## Objective:
The objective of the internship is to extract map components such as lane, road markings, etc. using AI/ML techniques.

## 1. Computer Vision Structural Techniques 
 - #### [*Intrinsic Calibration (using checkerboard)*](codes/Camera%20Calibration/Checkerboard/README.md)
 - #### [*Extrinsic Calibration (using arUco markers)*](codes/Camera%20Calibration/Aruco/README.md)
 
 - *Camera to Lidar Extrinsic Calibration*
 - [*Computer Vision Notes*](codes/Camera%20Calibration/README.md)

## 2. Road objects detection and segmentation using AI/ML techniques
This [AOD sheet](docs/AOD_Attributes.xlsx) contains different road objects for which we are aiming to find a suitable architecture.
* [Detection based architecture: *Mask_RCNN*](codes/Mask_RCNN/README.md)
* [Segmentation based architecture: *VPGNet*](codes/VPGNet/README.md)

## 3. Connecting the results of the previous task(detection and segmentation) to the real world physical coordinates
