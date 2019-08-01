#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:25:01 2019

@author: intern
"""

import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import numpy as np


"""Extract a folder of images from a rosbag.
"""
parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
parser.add_argument("bag_file", help="Input ROS bag.")
parser.add_argument("output_dir", help="Output directory.")
parser.add_argument("image_topic", help="Image topic.")

args = parser.parse_args()

print ("Extract images from %s on topic %s into %s" % (args.bag_file,
                                                      args.image_topic, args.output_dir))

bag = rosbag.Bag(args.bag_file, "r")
bridge = CvBridge()

numImg = 40
count = 0
count2 = 0
skipBy = 30

for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
    if(count%skipBy!=0):
	count += 1
	continue
    cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

    cv2.imwrite(os.path.join(args.output_dir, "frame%06i.png" % count2), cv_img)
    print ("Wrote image %i" % count2)

    count += 1
    count2 += 1
    if count2 == numImg:
        break

bag.close()

numImg = count2

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*4,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:4].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = []
rets = []

for i in range(0,numImg):
    images.append(args.output_dir+"/frame" + "{:0>6d}".format(i) + ".png")


for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (6,4),None)
    rets.append(ret)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (6,4), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey()
        cv2.destroyAllWindows()


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

tot_error = 0
errors = []

for i in range(0,len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    errors.append(error)
    tot_error += error

print "mean error: ", tot_error/len(objpoints)
print("camera matrix:")
print(mtx)
print("distortion coefficients:")
print(dist)
#print("individual errors:")
#print(errors)

