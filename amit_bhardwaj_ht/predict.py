# -*- coding: utf-8 -*-
"""
Created on Thu Jun 3 01:06:56 2020

@author: Amit B
"""

import cv2
import numpy as np
import os

from sklearn.externals import joblib


#
def imglist(path):
    return [os.path.join(path, f) for f in os.listdir(path)]

#Fill the placeholder empty lists with image path, classes, and add class ID number
def get_prediction(img_path): 
    clf, classes_names, stdSlr, k, voc = joblib.load("lincode.pkl")

    test_path = img_path
    testing_names = os.listdir(test_path)
    
    # Get path to all images and save them in a list
    # image_paths and the corresponding label in image_paths
    image_paths = []
    image_classes = []
    class_id = 0
    for testing_name in testing_names:
        dir = os.path.join(test_path, testing_name)
        class_path = imglist(dir)
        image_paths+=class_path
        image_classes+=[class_id]*len(class_path)
        class_id+=1
        
    # Create feature extraction and keypoint detector objects
    # Create List where all the descriptors will be stored
    des_list = []
    
    #BRISK is a good replacement to SIFT. 
    brisk = cv2.BRISK_create(30)
    
    for image_path in image_paths:
        im = cv2.imread(image_path)
        img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        #convert to 1x channel image (grayscale)
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kpts, des = brisk.detectAndCompute(img, None)
        des_list.append((image_path, des))   
        
    # Stack all the descriptors vertically in a numpy array
    descriptors = des_list[0][1]
    for image_path, descriptor in des_list[0:]:
        descriptors = np.vstack((descriptors, descriptor)) 
    
    # Calculate the histogram of features
    #vq Assigns codes from a code book to observations.
    from scipy.cluster.vq import vq    
    test_features = np.zeros((len(image_paths), k), "float32")
    for i in range(len(image_paths)):
        words, distance = vq(des_list[i][1],voc)
        for w in words:
            test_features[i][w] += 1
    
    # Perform Tf-Idf vectorization
    nbr_occurences = np.sum( (test_features > 0) * 1, axis = 0)
    
    # Scale the features
    #Standardize features by removing the mean and scaling to unit variance
    #Scaler (stdSlr comes from the pickled file we imported)
    test_features = stdSlr.transform(test_features)
    
    
    #true_class =  [classes_names[i] for i in image_classes]
    # Perform the predictions and report predicted class names. 
    predictions =  [classes_names[i] for i in clf.predict(test_features)]

    return predictions

if __name__ == '__main__':
    import argparse,json
    parser = argparse.ArgumentParser(description='Predict Image visibility for ID cards')
    parser.add_argument('image_file', help='The image path for prediction')
    args = parser.parse_args()
    response = get_prediction(args.image_file)
    print('<<< Prediction >>> \n',json.dumps(response, indent=4))


   


       
