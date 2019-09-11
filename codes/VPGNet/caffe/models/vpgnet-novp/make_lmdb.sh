../../build/tools/convert_driving_data /home/intern/devyash/VPGNet/caltech-lanes-dataset /home/intern/devyash/VPGNet/caltech-lanes-dataset/cordova2.txt LMDB_train
../../build/tools/compute_driving_mean LMDB_train ./driving_mean_train.binaryproto lmdb
../../build/tools/convert_driving_data /home/intern/devyash/VPGNet/caltech-lanes-dataset /home/intern/devyash/VPGNet/caltech-lanes-dataset/cordova1.txt LMDB_test
