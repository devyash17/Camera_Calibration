#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:57:05 2019

@author: intern
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = 'deploy.prototxt'
PRETRAINED = 'snapshots/split_iter_1000.caffemodel'

# load the model
caffe.set_mode_cpu()
#caffe.set_device(0)

#net = caffe.Net(MODEL_FILE, PRETRAINED, caffe.TEST)
net = caffe.Net(MODEL_FILE,1,weights=PRETRAINED)
#net = caffe.Classifier(MODEL_FILE, PRETRAINED,
#                       mean=np.load('mean.npy').mean(1).mean(1),
#                       channel_swap=(2,1,0),
#                       raw_scale=255,
#                       image_dims=(480, 640))
#print("successfully loaded classifier")

# test on a image
#IMAGE_FILE = 'input.png'
#input_image = caffe.io.load_image(IMAGE_FILE)
#res = net.forward({input_image})
# predict takes any number of images,
# and formats them for the Caffe net automatically
#pred = net.predict([input_image])