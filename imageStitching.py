import sys
import os
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2 as cv

def image_stitch(crop, upload_folder, output_folder):
    """ Stitch together images that is loaded into uplaod_folder"""
    print("[INFO] loading images...")
    images = []
    # Loop over the image paths, load each one, and add them to our images to stich list
    for file in os.listdir(upload_folder):
        file = upload_folder + "/" + file
        if file=='NULL':
            return False
        image = cv.imread(file)
        images.append(image)

    # Initialise OpenCV's image sticher object and then perform the image stitching
    print("[INFO] stitching images...")
    if imutils.is_cv2():
        stitcher = cv.createStitcher()
    else:
        stitcher = cv.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)

    # if the status is '0', then OpenCV successfully performed image stitching
    if status == 0:
        # check to see if we are meant to crop out the larger rectangular region from the sitched image
        if crop == "on":
            print("[INFO] cropping...")
            stitched = cv.copyMakeBorder(stitched, 10, 10, 10, 10, cv.BORDER_CONSTANT, (0, 0, 0))

            # convert the stitched image to grayscale and threshold it such taht all pixels greater than zero are set to 255 (foreground) while all other remain 0 (background)
            gray = cv.cvtColor(stitched, cv.COLOR_BGR2GRAY)
            thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY) [1]

            # find all external contours in the threshold image then find the 'largest' contour which will be the countor/outline of the stitcher image
            cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv.contourArea)

            # allocate memory for the mask which will contain the rectangular bounding box of the stitched image region
            mask = np.zeros(thresh.shape, dtype="uint8")
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

            #create two copies of the mask: one to serve as our actual minim rectangular region and anothr to serve as a counter
            # for how many pixels need to be removed to form the minimum rectangular region
            minRect = mask.copy()
            sub = mask.copy()

            # Keep looping until there are no non-zero pixels left in the subtracted images
            while cv.countNonZero(sub) > 0:
                # erode the minimum rectangular mask and then subtract the thresholded image from the minim retangular mask
                # So we can count if there are any non-zero pixels left
                minRect = cv.erode(minRect, None)
                sub = cv.subtract(minRect, thresh)
            
            # find contours in the minimum rectangular mask and extract the bounding box (x, y) - coordinates
            cnts = cv.findContours(minRect.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv.contourArea)
            (x, y, w, h) = cv.boundingRect(c)

            # use the bounding box coordinates to extract our final stitched image
            stitched = stitched[y:y + h, x:x + w]
        # write the output stitched image to disk
        cv.imwrite(output_folder + "/" + "output.png", stitched)

        return True
    
    else:
        print("[ERROR]: Unable to stitch images")
        return False
