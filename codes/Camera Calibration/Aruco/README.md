## Extrinsic Calibration (using arUco markers)

###### IMAGES
The images used for the extrinsic calibration of the cameras are images of an ArUco marker on a cardboard, as shown below,
![Sample Image](https://github.com/GuptaAbhinavv/MapmyIndia/blob/master/images/frame000000.png)

###### FLOWCHART

![Flowchart](https://github.com/GuptaAbhinavv/MapmyIndia/blob/master/images/flowchart2.png)

###### IMPORTANT FUNCTIONS
**_aruco.DetectMarkers()_**: Function from the aruco library of OpenCV, detects the corners of the aruco marker and returns the id of the aruco marker along with image coordinates of the corners of the marker.

**_cv2.stereoCalibrate()_**: Given the camera matrices, object points and the corresponding image points in images from both of the stereo cameras, it calculates the R, T, E, F i.e. Rotation Vector, Translation Vector,  Essential Matrix and the Fundamental Matrix respectively. R and T define the extrinsic calibration parameters between the two cameras.
###### RESULTS

###### VERIFICATION
The above results can be verified by calculating the value of-
##### x'Fx
which is supposed to be equal to zero according to the standard fundamental matrix equation. Closer the value to 0, accurate are the results.
**x'** and **x** in the above formula are the corresponding image coordinates in second and first image respectively.
