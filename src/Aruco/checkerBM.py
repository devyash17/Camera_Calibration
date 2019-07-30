#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:35:53 2019

@author: intern
"""
import os
import argparse

import cv2

#import rosbag
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge

import numpy as np
import cv2.aruco as aruco
import glob
import itertools

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*4,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:4].T.reshape(-1,2)
objp2 = np.zeros((2*2,3),np.float32)
objp2[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints1 = [] # 3d point in real world space
imgpoints1 = [] # 2d points in image plane.
objpoints2 = []
imgpoints2 = []
objpoints3 = []
imgpoints3 = []
objpoints4 = []
imgpoints4 = []

images1 = []
images2 = []
rets1 = []
rets2 = []
numImg = 943
count = 0
#for i in range(0,100):
#    images.append("/home/intern/devyash/intrinsic/pics/left/frame" + "{:0>6d}".format(i) + ".png")

for i in range(0,numImg):
    if(i%20!=0):
        continue
    images1.append("/home/intern/devyash/extrinsic/pic/left/frame" + "{:0>6d}".format(i) + ".png")
    images2.append("/home/intern/devyash/extrinsic/pic/right/frame" + "{:0>6d}".format(i) + ".png")
    count = count+1
    if count==40:
        break

images3 = []
images4 = []
count = 0
for i in range(0,numImg):
    if(i%10!=0):
        continue
    images3.append("/home/intern/devyash/extrinsic/arucoImg/left/frame" + "{:0>6d}".format(i) + ".png")    
    images4.append("/home/intern/devyash/extrinsic/arucoImg/right/frame" + "{:0>6d}".format(i) + ".png")    
    count = count+1
    if count==80:
        break

def extractDigits(lst): 
    return list(map(lambda el:[el], lst))

for (fname1,fname2) in zip(images1,images2):
    img1 = cv2.imread(fname1)
    img2 = cv2.imread(fname2)
#    cv2.imshow('img',img2)
#    cv2.waitKey()
#    cv2.destroyAllWindows()
    gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    retA, cornersA = cv2.findChessboardCorners(gray1, (6,4),None)
    rets1.append(retA)
    retB, cornersB = cv2.findChessboardCorners(gray2, (6,4),None)
    rets2.append(retB)
    # If found, add object points, image points (after refining them)
    if retA == True & retB == True:
        objpoints1.append(objp)
        corners2 = cv2.cornerSubPix(gray1,cornersA,(11,11),(-1,-1),criteria)
        imgpoints1.append(corners2)
        
        objpoints2.append(objp)
        corners2 = cv2.cornerSubPix(gray2,cornersB,(11,11),(-1,-1),criteria)
        imgpoints2.append(corners2)

        # Draw and display the corners
#        img = cv2.drawChessboardCorners(img, (6,4), corners2,ret)
#        cv2.imshow('img',img)
#        cv2.waitKey()
#        cv2.destroyAllWindows()
    

ret1, mtx1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(objpoints1, imgpoints1, gray1.shape[::-1],None,None)
ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(objpoints2, imgpoints2, gray2.shape[::-1],None,None)

#ptsLeft = np.int32(imgpoints1)
#ptsRight = np.int32(imgpoints2)

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints1, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2,  gray1.shape[::-1],criteria) 
#F, mask = cv2.findFundamentalMat(ptsLeft,ptsRight,cv2.FM_LMEDS)
#F, mask = cv2.findFundamentalMat(imgpoints1,imgpoints2,cv2.FM_LMEDS)
#tot_error = 0
#errors = []
#
#for i in range(0,len(objpoints)):
#    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
#    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
#    errors.append(error)
#    tot_error += error
#
#print "mean error: ", tot_error/len(objpoints)
#print("camera matrix:")
#print(mtx)
#print("distortion coefficients:")
#print(dist)
#print("individual errors:")
#print(errors)

#def draw(img, corners, imgpts):
#    corner = tuple(corners[0].ravel())
#    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
#    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
#    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
#    return img

#def draw(img, corners, imgpts):
#    imgpts = np.int32(imgpts).reshape(-1,2)
#    # draw ground floor in green
#    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
#    # draw pillars in blue color
#    for i,j in zip(range(4),range(4,8)):
#        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
#    # draw top layer in red color
#    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
#    return img
#
#criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#objp = np.zeros((6*4,3), np.float32)
#objp[:,:2] = np.mgrid[0:6,0:4].T.reshape(-1,2)
#
##axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
#axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
#                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])
#    
##for fname in glob.glob(args.output_dir+'/frame000003.png'):
#for fname in images:
#    img = cv2.imread(fname)
#    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#    ret, corners = cv2.findChessboardCorners(gray, (6,4),None)
#    #print('here')
##    print(ret)
#    if ret == True:
#        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
#
#        # Find the rotation and translation vectors.
#        _,rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
#        print 'rvecs:'
#        print(rvecs)
#        print
#        print 'tvecs:'
#        print(tvecs)
#        print
#        print '---------------------------------------------------'
#        # project 3D points to image plane
#        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
#
#        img = draw(img,corners2,imgpts)
#        cv2.imshow('img',img)
#        k = cv2.waitKey(0) & 0xff
#        cv2.destroyAllWindows()

###------------------ ARUCO TRACKER ---------------------------
set1 = []
corners1 = []
first = True
counter = []
rset = []
tset = []
## set dictionary size depending on the aruco marker selected
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
#board = aruco.GridBoard_create(4, 5, markerLength, 0, aruco_dict)
    
for (fname1,fname2) in zip(images3,images4):
        
#    ret, frame = cap.read()
    frame1 = cv2.imread(fname1)
    frame2 = cv2.imread(fname2)
    # operations on the frame
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    #parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    cornersA, idsA, rejectedImgPointsA = aruco.detectMarkers(gray1, aruco_dict, parameters=parameters)
    cornersB, idsB, rejectedImgPointsB = aruco.detectMarkers(gray2, aruco_dict, parameters=parameters)
    if((idsA is not None) & (idsB is not None)):
        if((len(idsA)==1) & (len(idsB)==1)):
##            cornersA = cv2.cornerSubPix(gray1,cornersA,(11,11),(-1,-1),criteria) #extractDigits(cornersA[0])
##            cornersB = cv2.cornerSubPix(gray2,cornersB,(11,11),(-1,-1),criteria) #extractDigits(cornersB[0])
#            objpoints3.append(objp2)
#            imgpoints3.append(cornersA)
#            objpoints4.append(objp2)
#            imgpoints4.append(cornersB)
       
#    set1.append(rejectedImgPoints)
#    corners1.append(corners)
#    aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            aruco.drawDetectedMarkers(frame1, cornersA)
#            # font for displaying text (below)
            font = cv2.FONT_HERSHEY_SIMPLEX
        
            # check if the ids list is not empty
            # if no check is added the code will crash
            if np.all(idsA != None) & np.all(idsB != None):
        #                print('in')
                # estimate pose of each marker and return the values
                # rvet and tvec-different from camera coefficients
                rvec1, tvec1 ,_ = aruco.estimatePoseSingleMarkers(cornersA, 0.05, mtx1, dist1)
                rvec2, tvec2 ,_ = aruco.estimatePoseSingleMarkers(cornersB, 0.05, mtx2, dist2)
#                rvec3, tvec3,_ = cv2.composeRT(rvec1,tvec1,rvec2,tvec2)
#                rset.append(rvec3)
#                tset.append(tvec3)
                #(rvec-tvec).any() # get rid of that nasty numpy value array error
        
                for i in range(0, idsA.size):
                    # draw axis for the aruco markers
                    aruco.drawAxis(frame1, mtx1, dist1, rvec1[i], tvec1[i], 0.1)
        
                # draw a square around the markers
                aruco.drawDetectedMarkers(frame1, cornersA)
        
        
                # code to show ids of the marker found
                strg = ''
                for i in range(0, idsA.size):
                    strg += str(idsA[i][0])+', '
        
                cv2.putText(frame1, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
        
        
            else:
                # code to show 'No Ids' when no markers are found
                cv2.putText(frame1, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
        
             #display the resulting frame
            cv2.imshow('frame',frame1)
            cv2.waitKey(10)
#            cv2.destroyAllWindows()
#            if cv2.waitKey(1) & 0xFF == ord('q'):
#                break
cv2.destroyAllWindows()

#imgpoints3 = [np.reshape(x, (4,1,2)) for x in imgpoints3]
#imgpoints4 = [np.reshape(x, (4,1,2)) for x in imgpoints4]
#
#retF, mtx11, dist11, mtx22, dist22,R2,T2,E2,F2 = cv2.stereoCalibrate(objpoints3, (imgpoints3), (imgpoints4),mtx1,dist1,mtx2,dist2,gray1.shape[::-1],criteria) 
#cornersB = cv2.cornerSubPix(gray2,cornersB,(11,11),(-1,-1),criteria)
