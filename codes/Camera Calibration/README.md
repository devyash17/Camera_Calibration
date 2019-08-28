Computer vision is an interdisciplinary scientific field that deals with how computers can be
made to gain high-level understanding from digital images or videos.

## Calculation of Camera Matrix
            x = PX

##### Basic Pinhole Model:

![image](https://user-images.githubusercontent.com/41137582/62455336-bcf8ac80-b793-11e9-93fb-ae19de7ff873.png)

##### Principal Point Offset:

![image](https://user-images.githubusercontent.com/41137582/62455485-15c84500-b794-11e9-8292-fc0a84136fab.png)

#### Camera Rotation and Translation:

![image](https://user-images.githubusercontent.com/41137582/62460478-ba9c4f80-b79f-11e9-8d21-b8faa27790ce.png)

#### Finite Projective Camera:

![image](https://user-images.githubusercontent.com/41137582/62455615-6d66b080-b794-11e9-9c27-7d13d3e5810f.png)

#### Distortion:
1. Radial: Straight lines appear curved.

![image](https://user-images.githubusercontent.com/41137582/62456048-3b098300-b795-11e9-9891-2a1dde356fcc.png)

2. Tangential: Occurs because image taking lens is not aligned perfectly parallel to the imaging plane. So some areas in image may look nearer than expected.

![image](https://user-images.githubusercontent.com/41137582/62456208-9471b200-b795-11e9-855b-6aa3167f4ed8.png)

So, 5 parameters are needed, known as the *distortion coefficients*.

## Epipolar Geometry and the Fundamental Matrix

#### Epipolar Geometry

The epipolar geometry between two views is essentially the geometry of the intersection of the image planes with the pencil of planes having the baseline as axis (the baseline is the line joining the camera centres).

![image](https://user-images.githubusercontent.com/41137582/62456536-40b39880-b796-11e9-9283-38d635aa59e5.png)

##### Definitions:
1. The **epipole** is the point of intersection of the line joining the camera centres (the baseline) with the image plane. Equivalently, the epipole is the image in one view of the camera centre of the other view.
2. An **epipolar plane** is a plane containing the baseline. There is a one-parameter family (a pencil) of epipolar planes.
3. An **epipolar line** is the intersection of an epipolar plane with the image plane. All epipolar lines intersect at the epipole. An epipolar plane intersects the left and right image planes in epipolar lines, and defines the correspondence between the lines.

#### Fundamental Matrix

The fundamental matrix(F) is the algebraic representation of epipolar geometry.
For an image point x and its corresponding point in the other image x',

![image](https://user-images.githubusercontent.com/41137582/62456766-d2230a80-b796-11e9-8d50-cb5e53ef1665.png)

##### Properties:
1. F is a rank 2 homogeneous matrix with 7 degrees of freedom.
2. Epipolar Lines: `l' = Fx` is the epipolar line corresponding to x.
                   `l = Fx'` is the epipolar line corresponding to x’.
3. Epipoles: ![image](https://user-images.githubusercontent.com/41137582/62457737-07c8f300-b799-11e9-83ac-d31bf58a029a.png)

#### Essential Matrix

The essential matrix(E) is the specialization of the fundamental matrix to the case of normalized image coordinates. The essential matrix has fewer degrees of freedom, and additional properties, compared to the fundamental matrix.

![image](https://user-images.githubusercontent.com/41137582/62458360-575bee80-b79a-11e9-974d-cdb4814e759e.png)

Normalized image coordinates :  ![image](https://user-images.githubusercontent.com/41137582/62458422-7fe3e880-b79a-11e9-8c6f-1362036d7707.png)

## Reconstruction of Cameras and Sttructure

#### Outline:
1. Compute the fundamental matrix from point correspondences.
2. Compute the camera matrices from the fundamental matrix.
3. For each point correspondence `x <--> x'`  compute the point in space that projects to these two image points.

#### Computation of the Fundamental Matrix

Given a set of correspondences `x <--> x'` in two images the fundamental matrix F satisfies the
condition ![image](https://user-images.githubusercontent.com/41137582/62456766-d2230a80-b796-11e9-8d50-cb5e53ef1665.png)
With the `x and x'` known, this equation is linear in the (unknown) entries of the matrix F. Infact, each point correspondence generates one linear equation in the entries of F. Given at least 8 point correspondences it is possible to solve linearly for the entries of F up to scale (a non-linear solution is available for 7 point correspondences).

#### Computation of the Camera Matrices

A pair of camera matrices `P and P'` corresponding to the fundamental matrix F is easily computed using the direct formula as shown earlier.

#### Triangulation

![image](https://user-images.githubusercontent.com/41137582/62459240-82dfd880-b79c-11e9-80eb-15ca5ba465a8.png)

The image points `x and x'` back project to rays. If the epipolar constraint ![image](https://user-images.githubusercontent.com/41137582/62456766-d2230a80-b796-11e9-8d50-cb5e53ef1665.png) is satisfied, then these two rays lie in a plane, and so intersect in a point X in 3-space.
The only points in 3-space that cannot be determined from their images are points on the baseline between the two cameras. In this case, the back-projected rays are collinear (both being equal to the baseline) and intersect along their whole length.

#### Reconstruction Ambiguity

![image](https://user-images.githubusercontent.com/41137582/62459804-eddddf00-b79d-11e9-99fe-b8f096bc57be.png)

##### 1. Position Ambiguity

It is impossible based on the images alone to estimate the absolute location and pose of the scene w.r.t. a 3D world coordinate frame.

![image](https://user-images.githubusercontent.com/41137582/62459916-2bdb0300-b79e-11e9-95ba-665562213077.png)

##### 2. Scale Ambiguity

It is impossible based on the images alone to estimate the absolute scale of the scene (i.e. house height).

![image](https://user-images.githubusercontent.com/41137582/62459976-5462fd00-b79e-11e9-8734-36b2cb7ed008.png)

#### The projective reconstruction theorem

We can compute a projective reconstruction of a scene from 2 views based on image correspondences alone.We don’t have to know anything about the calibration or poses of the cameras.
Assume we determine matching points `x and x'`. Then we can compute a unique fundamentalmatrix F. The recovered camera matrices are not unique: (P1, P’1), (P2, P’2), etc. Hence the reconstruction is not unique. There exists a projective transformation H such that

![image](https://user-images.githubusercontent.com/41137582/62460094-b15eb300-b79e-11e9-817b-c0fa021fc911.png)

![image](https://user-images.githubusercontent.com/41137582/62460291-419cf800-b79f-11e9-9c87-0adf282a828c.png)

If the reconstruction is derived from real images,there is a true reconstruction that can produce the actual points `Xi` of the scene.
