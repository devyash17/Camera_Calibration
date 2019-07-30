Three programs are there in total.
Here are the details regarding their functionalities and the steps to run them.

1) serial.py: It selects the first 40 images out of 1466 images. Therefore, the mean error is low.
2) bagToIntrinsic.py: It selects every 30th image to maintain variability in images.
3) bagToIntr.py: It takes into account the similarity between images before adding them to the set.

How to run:
python program_name.py bag_file.bag path_name image_topic

where
program_name is one of the above 3 programs
bag_file is the name of the bag file
path_name is the path of the directory where images will be stored e.g. /home/intern/devyash/intrinsic/pics1/left
image_topic is the topic of the image e.g. /frontNear/left/image_raw

Note that the directory for storing the left and right images needs to be created before running the code. 

