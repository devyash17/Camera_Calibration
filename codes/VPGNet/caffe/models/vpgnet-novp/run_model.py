import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time # time the execution time

import caffe
import cv2

import shelve # store workspace

workspace_root = 'workspace/'
if not os.path.exists(os.path.join(os.getcwd(), workspace_root)):
    os.mkdir(workspace_root)

model = 'deploy.prototxt' # original deploy, no pruning
pretrained = 'snapshots_new/split_iter_10000.caffemodel'


caffe.set_mode_gpu()
caffe.set_device(0)

net = caffe.Net(model, pretrained, caffe.TEST)

for it in range(1,101):
    # input_img = '/home/intern/devyash/VPGNet/caltech-lanes-dataset/cordova2/f'+"{:0>5d}".format(it)+'.png'
    input_img = 'formatted/'+str(it)+'.jpg'
    img = caffe.io.load_image(input_img)

    print("Start timing!")
    t = time.time()

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost dimension
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2, 1, 0))
    transformed_img = transformer.preprocess('data', img) # swap R, B channel, the final input to the network should be RGB

    net.blobs['data'].data[...] = transformed_img
    t1 = time.time()
    for i in range(1):
        net.forward()
        
    print("forward propagation time: ", time.time() - t1)

    dt = time.time() - t
    print("Timing ends! Process time:", dt)


    # Visualize the test result:

    img = cv2.imread(input_img)
    for i in range(3):
        for j in range(transformed_img.shape[1]):
            for k in range(transformed_img.shape[2]):
                img[j, k, i] = transformed_img[i, j, k]
    
    classification = net.blobs['multi-label'].data
    attr = net.blobs['multi-label'].data[0,:1]
    print classification.shape
    print attr.shape
    classes = []


    # create color for visualizing classification
    def color_options(x):
        return {
            1: (0, 255, 0), # green color
            2: (255, 0, 0), # blue
            3: (0, 0, 255), # red
            4: (0, 0, 0)
        }[x]

    # visualize classification
    y_offset_class = 1 # offset for classification error
    x_offset_class = 1
    grid_size = img.shape[0]/60
    for i in range(60):
        classes.append([])
        for j in range(80):
            max_value = 0.0
            maxi = 0
            for k in range(64):
                if classification[0, k, i, j] > max_value:
                    max_value = classification[0, k, i, j]
                    maxi = k

            classes[i].append(maxi)
            if maxi != 0:
                pt1 = ((j + y_offset_class)*grid_size, (i+x_offset_class)*grid_size)
                pt2 = ((j + y_offset_class)*grid_size+grid_size, (i+x_offset_class)*grid_size+grid_size)
                # cv2.circle(img,pt1,2,color_options(maxi),2)
                cv2.rectangle(img, pt1, pt2, color_options(maxi), 2)
                if maxi not in [1, 2, 3, 4]:
                    print("ERROR OCCURRED: an unknown class detected!")             

    cv2.imwrite(workspace_root + str(it) + ".png", img) 