# Camera_Calibration


## Calibration Techniques:
    - Intrinsic (using checkerboard)
    - Extrinsic (using ArUco Markers)
    - Lidar & Camera together

### Intrinsic (using checkerboard)

#### Data Preprocessing:

###### BAG FILES
A bag is a file format in ROS for storing ROS message data. Bags -- so named because of their .bag extension -- have an important role in ROS, and a variety of tools have been written to allow you to store, process, analyze, and visualize them.
Bags are typically created by a tool like rosbag, which subscribe to one or more ROS topics, and store the serialized message data in a file as it is received. These bag files can also be played back in ROS to the same topics they were recorded from or even remapped to new topics.

We can use the following command to get the details of a bag file:
rosbag info foo.bag
The output might look something like this:

![img](https://answers.ros.org/upfiles/14701677325167827.png)
                                           Fig. 1

 ###### IMAGE EXTRACTION
The images contained in the bag file can be extracted using the below given code snippet:
Command to run the below code:
                 python program_name.py bag_file.bag path_name image_topic
bag_file: name of the bag file
path_name: path of the directory where images will be stored.
image_topic: topic of the image e.g. /frontNear/left/image_raw/

![Screenshot from 2019-07-31 11-39-17](https://user-images.githubusercontent.com/41137582/62187781-13c34800-b388-11e9-874a-87d50942445b.png)

                             Fig. 2: To extract the images out of a given bag file


Run the above code and store the corresponding images in the left and right directories(based on the topics of the messages).
Note that the directory for storing the left and right images needs to be created before running the code. 

###### Calculating Intrinsic parameters:

*FLOWCHART*
 
 ![Screenshot from 2019-07-31 11-45-42](https://user-images.githubusercontent.com/41137582/62188019-c3001f00-b388-11e9-9a18-5b71948e3e86.png)


*IMPORTANT FUNCTIONS USED*

- compare_ssim: Compute the mean structural similarity index between two images.

- cv2.findChessboardCorners: Finds positions of the internal corners of the chessboard. Returns a boolean value depending on if the given shape of corners are found, also returns location of the corners if true.

- cv2.cornerSubPix: The function iterates to find the sub-pixel accurate location of corners or radial saddle points.

- cv2.drawChessboardCorners: Renders the detected chessboard corners.

- cv2.calibrateCamera: Finds the camera intrinsic and extrinsic parameters from several views of a calibration pattern. Returns the rotation and translation matrix corresponding to each pattern. Also returns the camera intrinsic and distortion vector corresponding to lowest reprojection error.

- cv2.projectPoints: Projects 3D points to an image. Used for calculating the reprojection error.

- cv2.norm: Calculates the absolute or relative difference norm between the given image matrices. 

*RESULTS*
The algorithm takes 40 patterns from the given sample to calibrate the given camera. To cover all the possible orientations of the checkerboard, the selected sample images must be different in orientations. Three techniques have been used to select such samples:

    1. Simply selecting first 40 images: Very low reprojection error suggests a possibility of images with similar orientations of the board been selected for calibration.  Therefore, a technique to select “good” images from the sample is required.
    
   ![1](https://user-images.githubusercontent.com/41137582/62188337-a9aba280-b389-11e9-96da-fe581ef976e1.png)



    2. Skipping a few images after each image: Another approach we came up with is to skip about 20 to 25 images after selecting one so as to keep the variation amongst the selected images. The results obtained on including every 30th image are:
    
   ![Screenshot from 2019-07-31 11-55-06](https://user-images.githubusercontent.com/41137582/62188447-13c44780-b38a-11e9-84cd-3a6c95fe0ee8.png)

 

    3. Calculating Structural Similarity index and filtering: Involves calculating the structural similarity index to compare every image with the previous image selected for calibration, based on the assumption that each image is more likely to be similar to the image previous to it as compared to others. A threshold value of SSIM is selected arbitrarily and the images with their value higher than the threshold are rejected. The results, obviously, are highly sensitive to the threshold value. 
      a. Results with threshold SSIM = 0.65
![Screenshot from 2019-07-31 11-56-09](https://user-images.githubusercontent.com/41137582/62188486-37878d80-b38a-11e9-87d0-f4c196e7a0fb.png)

      b.   Results with threshold SSIM = 0.62
![Screenshot from 2019-07-31 11-56-58](https://user-images.githubusercontent.com/41137582/62188520-525a0200-b38a-11e9-971a-56fca1fddd92.png)
