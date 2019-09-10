## [VPGNet: Vanishing Point Guided Network for Lane and Road Marking Detection and Recognition]

International Conference on Computer Vision (ICCV) 2017

![teaser](https://user-images.githubusercontent.com/41137582/64516163-a0f4a780-d30b-11e9-8326-6b04c820c87c.png)

In this paper, we propose a unified end-to-end trainable multi-task network that jointly handles lane and road marking detection and recognition that is guided by a vanishing point under adverse weather conditions. We tackle rainy and low illumination conditions, which have not been extensively studied until now due to clear challenges. For example, images taken under rainy days are subject to low illumination, while wet roads cause light reflection and distort the appearance of lane and road markings. At night, color distortion occurs under limited illumination. As a result, no benchmark dataset exists and only a few developed algorithms work under poor weather conditions. To address this shortcoming, we build up a lane and road marking benchmark which consists of about 20,000 images with 17 lane and road marking classes under four different scenarios: no rain, rain, heavy rain, and night. We train and evaluate several versions of the proposed multi-task network and validate the importance of each task. The resulting approach, VPGNet, can detect and classify lanes and road markings, and predict a vanishing point with a single forward pass. Experimental results show that our approach achieves high accuracy and robustness under various conditions in real-time (20 fps). The benchmark and the VPGNet model will be publicly available. 


### Supplementary
+ https://www.youtube.com/watch?v=jnewRlt6UbI


### Baseline Usage
1) Clone the repository

    ```Shell
    git clone https://github.com/SeokjuLee/VPGNet.git
    ```

2. Prepare dataset from Caltech Lanes Dataset.<br/>
(Our dataset is currently being reviewed by Samsung Research. This baseline doesn't need VP annotations.)
    - Download [Caltech Lanes Dataset](http://www.mohamedaly.info/datasets/caltech-lanes).
    - Organize the file structure as below.
    ```Shell
    |__ VPGNet
        |__ caffe
        |__ caltech-lanes-dataset
            |__ caltech-lane-detection/matlab
            |__ cordova1
            |__ cordova2
            |__ washington1
            |__ washington2
            |__ vpg_annot_v1.m
    ```
    - Generate list files using 'caltech-lanes-dataset/vpg_annot_v1.m'. Arrange training and validation sets as you wish. 

3. Caffe compliation
    - Compile our Caffe codes following the [instructions](http://caffe.berkeleyvision.org/installation.html).
    - Move to 'caffe/models/vpgnet-novp'. This is our workspace.

4. Make LMDB
    - Change paths in 'make_lmdb.sh' and run it. The LMDB files would be created.
    
5. Training
    - Run 'train.sh'

### Annotation Examples

![image](https://user-images.githubusercontent.com/41137582/64606340-a7565280-d3e3-11e9-9833-61142d90b8a6.png)
The above annotation can be visualized by running the script make_lmdb.sh

### Progress till now

I trained the model on [Caltech Lanes Dataset](http://www.mohamedaly.info/datasets/caltech-lanes) with the following configurations:
</br>[*`test_iter`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#test_iter): 2
</br>[*`test_interval`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#test_interval): 10
</br>[*`base_lr`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#base_lr): 0.005
</br>[*`lr_policy`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#lr_policy): step
</br>[*`gamma`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#gamma): 0.1
</br>[*`max_iter`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#max_iter): 1000
</br>[*`momentum`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#momentum): 0.9
</br>[*`solver_mode`*](https://github.com/BVLC/caffe/wiki/Solver-Prototxt#solver_mode): CPU

#### Loss vs Iterations:
![image](https://user-images.githubusercontent.com/41137582/64609917-a3c6c980-d3eb-11e9-9798-34cc7b2842a6.png)
![image](https://user-images.githubusercontent.com/41137582/64609948-bf31d480-d3eb-11e9-898f-3ae223bbab27.png)
![image](https://user-images.githubusercontent.com/41137582/64609989-d4a6fe80-d3eb-11e9-9583-864d5f613be6.png)

As seen in the graph above, the loss functions for the three branches of the network are converging in nature.</br>L = w<sub>1</sub>L<sub>reg</sub> + w<sub>2</sub>L<sub>om</sub> + w<sub>3</sub>L<sub>ml</sub> + w<sub>4</sub>L<sub>vp</sub>
</br> where L<sub>reg</sub> is a grid regression L1 loss, L<sub>om</sub> and L<sub>ml</sub> and L<sub>vp</sub> are are cross entropy losses in each branch of the network.
