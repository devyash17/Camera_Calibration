#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:35:53 2019

@author: intern
"""
import cv2
import numpy as np
import cv2.aruco as aruco

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*4,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:4].T.reshape(-1,2)
objp2 = np.zeros((2*2,3),np.float32)
objp2[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
# for checkerboard
objpoints1 = [] # 3d point in real world space
imgpoints1 = [] # 2d points in image plane.
objpoints2 = []
imgpoints2 = []


images1 = []
images2 = []
rets1 = []
rets2 = []
numImg = 943
count = 0

for i in range(0,numImg):
    if(i%20!=0):
        continue
    images1.append("/home/intern/devyash/extrinsic/pic/left/frame" + "{:0>6d}".format(i) + ".png")
    images2.append("/home/intern/devyash/extrinsic/pic/right/frame" + "{:0>6d}".format(i) + ".png")
    count = count+1
    if count==40:
        break

for (fname1,fname2) in zip(images1,images2):
    img1 = cv2.imread(fname1)
    img2 = cv2.imread(fname2)
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

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints1, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2,  gray1.shape[::-1],criteria) 

#for aruco markers
images3 = []
images4 = []
count = 0
rset = []
tset = []
dists = []
objpoints3 = []
imgpoints3 = []
objpoints4 = []
imgpoints4 = []

for i in range(0,numImg):
#    if(i%10!=0):
#        continue
    images3.append("/home/intern/devyash/extrinsic/arucoImg/left/frame" + "{:0>6d}".format(i) + ".png")    
    images4.append("/home/intern/devyash/extrinsic/arucoImg/right/frame" + "{:0>6d}".format(i) + ".png")    
    count = count+1
    if count==200:
        break

## set dictionary size depending on the aruco marker selected
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
#board = aruco.GridBoard_create(4, 5, markerLength, 0, aruco_dict)
    
for (fname1,fname2) in zip(images3,images4):
        
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
            objpoints3.append(objp2)
            imgpoints3.append(cornersA)
            objpoints4.append(objp2)
            imgpoints4.append(cornersB)
       

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
                r1,_ = cv2.Rodrigues(rvec1)
                r2,_ = cv2.Rodrigues(rvec2)
                
                tmp1 = cv2.Rodrigues(np.dot(r1,r2));
                rset.append(tmp1[0])
                tmp1 = np.dot(r2,np.reshape(tvec1[0],(3,1)))
                tmp2 = np.reshape(tvec2[0],(3,1))
                tmp1[0][0] += tmp2[0][0]
                tmp1[1][0] += tmp2[1][0]
                tmp1[2][0] += tmp2[2][0]
                tset.append(tmp1)
                
#                r1inv = np.linalg.inv(r1)
#                r2inv = np.linalg.inv(r2)
#                c1 = (-1)*np.dot(r1inv,np.reshape(tvec1[0],(3,1)))
#                c2 = (-1)*np.dot(r2inv,np.reshape(tvec2[0],(3,1)))
#                dist = np.linalg.norm(c1-c2)*360
#                dists.append(dist)
        
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
            cv2.waitKey(5)
            
cv2.destroyAllWindows()

# calculating R and T by taking average
for i in range(1,len(rset)):
    rset[0][0][0] += rset[i][0][0]
    rset[0][1][0] += rset[i][1][0]
    rset[0][2][0] += rset[i][2][0]

for i in range(1,len(tset)):
    tset[0][0][0] += tset[i][0][0]
    tset[0][1][0] += tset[i][1][0]
    tset[0][2][0] += tset[i][2][0]

rset[0][0][0] /= len(rset)
rset[0][1][0] /= len(rset)
rset[0][2][0] /= len(rset)
tset[0][0][0] /= len(tset)
tset[0][1][0] /= len(tset)
tset[0][2][0] /= len(tset)

R1 = cv2.Rodrigues(rset[0])[0]
T1 = tset[0]

imgpoints3 = [np.reshape(x, (4,1,2)) for x in imgpoints3]
imgpoints4 = [np.reshape(x, (4,1,2)) for x in imgpoints4]

retF, mtx11, dist11, mtx22, dist22,R2,T2,E2,F2 = cv2.stereoCalibrate(objpoints3, (imgpoints3), (imgpoints4),mtx1,dist1,mtx2,dist2,gray1.shape[::-1],criteria) 
