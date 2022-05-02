from multiprocessing.connection import wait
import os
import argparse
import cv2
from DetectorAPI import Detector


def blurBoxes(image, boxes):
    """
    Argument:
    image -- the image that will be edited as a matrix
    boxes -- list of boxes that will be blurred each element must be a dictionary that has [id, score, x1, y1, x2, y2] keys

    Returns:
    image -- the blurred image as a matrix
    """

    for box in boxes:
        # unpack each box
        x1, y1 = box["x1"], box["y1"]
        x2, y2 = box["x2"], box["y2"]

        # crop the image due to the current box
        sub = image[y1:y2, x1:x2]

        # apply GaussianBlur on cropped area
        blur = cv2.blur(sub, (25, 25))

        # paste blurred image on the original image
        image[y1:y2, x1:x2] = blur

    return image



# assign model path and threshold
model_path = 'face.pb'
threshold = 0.4

# create detection object
detector = Detector(model_path=model_path, name="detection")

# open image
image = cv2.imread('input.jpg')

# real face detection
faces = detector.detect_objects(image, threshold=threshold)
print("Faces detected")

# apply blurring
image = blurBoxes(image, faces)
print("Faces blurred")

# show image
#cv2.imshow('blurred', image)

# if image will be saved then save it
cv2.imwrite('output.jpg', image)
print('Image has been saved successfully at', 'output.jpg','path')
    

# loop infinitely and do nothing
