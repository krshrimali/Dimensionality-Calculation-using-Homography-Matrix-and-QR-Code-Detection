#!/usr/bin/env python

'''
Book Dimension Approximation
==================

Approximate the height and width of the book, using Homography, Feature Detection and zbar
for QR detection. Tracker used from plane_tracker.py in opencv modules.

Instructions
===================
    (Double left click to select points)
  1) Select corner points of the book cover. Click on the points, starting in this order:
                    top left -> top right -> bottom right -> bottom left
  2) Corrected image will be shown in front of you (perspective correction).
  3) Select corner points of the relative shape. (test case - "AMBIGUITIES") in this order:
                    top left -> top right -> bottom right -> bottom left
  4) If the program quits, then it means that you haven't selected all 8 points.
  5) The program will then show real width and height of all the edges.

[Note: Here, text has to be "AMBIGUITIES", if not then update the actual lengths in main method.]

Usage
-----
book_dimensions_new.py --image [<image source>] --real_width [<real_width>] --real_height [<real_height>]

real_height and real_weight : of the relative shape [for test, 1.1 and 14 respectively of "AMBIGUITIES"]

Select a plane representing book's corners, QR code scanners. Homography Feature Detection done,
if QR code in the book. Ratio used to calculate the height and width of the book.
'''
# Python 2/3 compatibility
from __future__ import print_function
import argparse
import sys
# import cv2 as cv
import cv2
import math
import numpy as np
from utils import *

if __name__ == '__main__':
    # Print documentation in the beginning
    print(__doc__)

    # Add arguments for command line intake
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to image")
    ap.add_argument("-w", "--real_width", required = True, help = "Real Width")
    ap.add_argument("-H", "--real_height", required = True, help = "Real Height")

    try:
        args = vars(ap.parse_args())

        real_width = args["real_width"]
        real_height = args["real_height"]

        img = cv2.imread(args["image"])

    except:
        print("Check if proper arguments are given.")
        print("Quitting")
        sys.exit()

    # Optional
    # resizing, reducing higher resolution
    clone = cv2.resize(img, (0,0), fx=0.125, fy=0.125) 

    size = (300, 400, 3)

    # create numpy array (zero matrix) with given size
    img_dest = np.zeros(size, np.uint8)

    # reference points for destination image
    refPt_dst = np.array(
                       [
                        [0,0],
                        [size[0] - 1, 0],
                        [size[0] - 1, size[1] -1],
                        [0, size[1] - 1 ]
                        ], dtype=float
                       )

    # cv.namedWindow("image")
    cv2.imshow("Image", clone)

    # set mouse call back event for left button double click
    points = get_four_points(clone)

    # Calculation of Homography matrix
    h, status = cv2.findHomography(points, refPt_dst)

    # Warping source image to destination image
    img_dest = cv2.warpPerspective(clone, h, size[0:2])

    # Save the corrected image for future reference
    cv2.imwrite("images/book_perspective.jpg", img_dest)

    # # get book corners
    # refPt = get_four_points(img_dest)

    refPt = [[0, 0], [img_dest.shape[1], 0], [img_dest.shape[1], img_dest.shape[0]], [0, img_dest.shape[0]]]
    # refPt = get_four_points(img_dest) # book corners selected earlier
    # get reference image corners
    refPt_reference = get_four_points(img_dest)

    # print(refPt)
    # calculate edge lengths based on recorded points
    Dimensions_width_top = distance(refPt[0], refPt[1])
    Dimensions_width_bottom = distance(refPt[2], refPt[3])

    Actual_Dimensions_top_width = distance(refPt_reference[1], refPt_reference[0])
    Actual_Dimensions_bottom_width = distance(refPt_reference[2], refPt_reference[3])

    Dimensions_height_left = distance(refPt[0], refPt[3])
    Dimensions_height_right = distance(refPt[2], refPt[1])

    Actual_Dimensions_left_height = distance(refPt_reference[0], refPt_reference[3])
    Actual_Dimensions_right_height = distance(refPt_reference[1], refPt_reference[2])

    # find actual edge lengths
    width_top = Dimensions_width_top / float(Actual_Dimensions_top_width) * float(real_width)
    width_bottom = Dimensions_width_bottom / float(Actual_Dimensions_bottom_width) * float(real_width)

    height_left = Dimensions_height_left / float(Actual_Dimensions_left_height) * float(real_height)
    height_right = Dimensions_height_right / float(Actual_Dimensions_right_height) * float(real_height)

    print("Top Edge width: ", width_top)
    print("Bottom Edge width: ", width_bottom)
    print("Left Edge height: ", height_left)
    print("Right Edge height: ", height_right)
