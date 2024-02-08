import sys
import argparse
from imutils import paths
import numpy as np
import imutils
import cv2


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i","--images", type=str, required=True, help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True, help="path to output image")
#ap.add_argument("-i", "--images images/4k_Lake_Pano")
#ap.add_argument("-o", "--output images/output/output_4k_Lake_Pano.png")
args = vars(ap.parse_args())

# Grab the paths to the input i,ages and initialze our images list
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"])))
images = []

# Loop over the image paths, load each one, as add them to our images to stitch list
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

# Initialise OpenCV's image stitcher object and then perform the image stitching
print("[INFO] stitching images...")
if imutils.is_cv3():
    stitcher = cv2.createStitcher()
else:
    stitcher = cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# If the status is '0', then OpenCV successfully performed image stitching
if status == 0:
    cv2.imwrite(args["output"], stitched)

    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
else:
    print("[INFO] image stitching failed ({})".format(status))