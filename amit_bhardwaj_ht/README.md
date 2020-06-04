***


# Classifying the visibility of ID cards in photos

The folder images inside data contains several different types of ID documents taken in different conditions and backgrounds. The goal is to use the images stored in this folder and to design an algorithm that identifies the visibility of the card on the photo (FULL_VISIBILITY, PARTIAL_VISIBILITY, NO_VISIBILITY).

## Data

Inside the data folder you can find the following:

### 1) Folder images
A folder containing the challenge images.

### 2) gicsd_labels.csv
A CSV file mapping each challenge image with its correct label.
	- **IMAGE_FILENAME**: The filename of each image.
	- **LABEL**: The label of each image, which can be one of these values: FULL_VISIBILITY, PARTIAL_VISIBILITY or NO_VISIBILITY. 


## Dependencies

pip insall -r requirement.txt

## Run Instructions

python train.py
python predict.py <training_images_path>

## Approach

1.Data exploration and preprocessing determined that out of the 800 images provided (each size; 192x192), 646 were labelled FULL_VISIBILITY, 123 were labelled PARTIAL_VISIBILITY and 31 were labelled NO_VISIBILITY. The data contained no missing values or duplications.
2.Images were split in to 3 separate folders by their visibility classification.
3.Data augmentation applied to increase the training dataset for PARTIAL_VISIBILITY (5-fold) and NO_VISIBILITY (10-fold) via various geometric transformations. This included; rotations, translations, zooms, brightness changes, perspective tilts and horizontal/vertical flips.
4.New augmented training dataset for PARTIAL_VISIBILITY and NO_VISIBILITY replaced their original training dataset before splitting the images into train-validate-split batches (70:15:15).
5.Images converted from RGB into single-channel arrays for feature engineering.
6.Get the training classes names and store them in a list,Here we use folder names for class names
7.Create feature extraction and keypoint detector objects in a List where all the descriptors will be stored
8.Perform k-means clustering and vector quantization
9.Perform Tf-Idf vectorization
10.Standardize features by removing the mean and scaling to unit variance(normalization)
11.Train an algorithm to discriminate vectors corresponding to FULL_VISIBILITY, PARTIAL_VISIBILITY and NO_VISIBILITY 

## Future Work

1. automating the task of image gathering.
2. Try with more deep learning models rather than traditional ML models.
3. Experimenting with image processing.