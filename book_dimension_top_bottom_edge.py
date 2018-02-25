#!/usr/bin/env python

'''
Book Dimension Approximation
==================

Approximate the height and width of the book, using Homography, Feature Detection and zbar
for QR detection. Tracker used from plane_tracker.py in opencv modules.

Instructions
===================

1) (For top edge) Select a small rectangle, starting point being the (initial) edge point and ending to the
end point of the edge. [This is used to find the edge length]
2) Repeat step 1 for bottom edge.
3) Select the text, to be used for Step 1. [Here the text will be QR code later]
4) Repeat step 3, as it is.
[Note: Here, text has to be "AMBIGUITIES", if not then update the actual lengths in main method.]

Usage
-----
book_length_detection.py [<image source>]

Select a plane representing book's corners, QR code scanners. Homography Feature Detection done,
if QR code in the book. Ratio used to calculate the height and width of the book.
'''

# Python 2/3 compatibility
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import math

# local modules
import video
from video import presets
import common
from common import getsize, draw_keypoints
from plane_tracker import PlaneTracker

def distance(x0,x1,y0,y1):
    sq1 = (x0 - x1)**2
    sq2 = (y0 - y1)**2
    return math.sqrt(abs(sq1 + sq2))

class App:
    def __init__(self, src):
        image = cv.imread(src, 1)
        small = cv.resize(image, (0,0), fx=0.125, fy=0.125) # resizing the image, as high resolution image taken
        self.frame = small
        self.paused = False
        self.tracker = PlaneTracker()

        cv.namedWindow('Selected Region')
        # cv.setMouseCallback('Selected Region', self.draw_circle_corner)
        self.rect_sel = common.RectSelector('Selected Region', self.on_rect)

    def on_rect(self, rect):
        self.tracker.clear()
        self.tracker.add_target(self.frame, rect)

    def run_original(self):

        while True:
            playing = not self.paused and not self.rect_sel.dragging
            # flag used to quit imaging, when the size detected.
            flag = 0
            # if playing or self.frame is None:
            #     # ret, frame = self.cap.read()
            #     if not ret:
            #         break
            #     self.frame = frame.copy()
            # size of the frame (image) - used to draw rectangle
            w, h = getsize(self.frame)
            vis = np.zeros((h, w*2, 3), np.uint8)
            # copy to the image (original)
            vis[:h,:w] = self.frame
            if len(self.tracker.targets) > 0:
                target = self.tracker.targets[0]
                vis[:,w:] = target.image
                draw_keypoints(vis[:,w:], target.keypoints)
                x0, y0, x1, y1 = target.rect # rectangle coordinates
                cv.rectangle(vis, (x0+w, y0), (x1+w, y1), (0, 255, 0), 2) # green line drawn
                # finding the width of the region
                width_region = distance(x0, x1, y0, y1)
                flag = 1 # set flag = 1, quit the program!
            self.rect_sel.draw(vis)
            cv.imshow('Selected Region', vis) # show the image
            ch = cv.waitKey(1)
            if ch == 27 or flag == 1:
                print("Quitting")
                return width_region

    def run(self, Cover_Dimensions, Actual_Dimensions):
        '''
        Runs the program, of selection of the image's region. Approximates the
        dimensions of the cover based on given dimensions.
        '''
        while True:
            # flag used to quit imaging, when the size detected.
            flag = 0
            playing = not self.rect_sel.dragging

            # get size of the book cover
            w, h = getsize(self.frame)
            vis = np.zeros((h, w*2, 3), np.uint8)
            vis[:h,:w] = self.frame

            if len(self.tracker.targets) > 0:
                target = self.tracker.targets[0]
                vis[:,w:] = target.image
                draw_keypoints(vis[:,w:], target.keypoints)
                x0, y0, x1, y1 = target.rect # get the selected region coordinates
                cv.rectangle(vis, (x0+w, y0), (x1+w, y1), (0, 255, 0), 2)

                Region_Dimensions = [x1 - x0, y1 - y0]
                print("Region_Dimensions:", Region_Dimensions)
                # Ratio of the cover dimensions (width) to region dimensions (width)
                # similarly for height
                ratio_width = float(Cover_Dimensions)/(Region_Dimensions[0])

                # Hard coded the actual width and height of the region.
                # Actual width (in cm) = 14
                # Actual height (in cm) = 1.1
                width_of_book = ratio_width * Actual_Dimensions[0]
                # height_of_book = ratio_height * Actual_Dimensions[1]

            # Optional (useful in case of video source)
            if playing:
                tracked = self.tracker.track(self.frame)
                if len(tracked) > 0:
                    tracked = tracked[0]
                    cv.polylines(vis, [np.int32(tracked.quad)], True, (255, 255, 255), 2)
                    for (x0, y0), (x1, y1) in zip(np.int32(tracked.p0), np.int32(tracked.p1)):
                        cv.line(vis, (x0+w, y0), (x1, y1), (0, 255, 0))
                        print("Detected")
                        # break when the region is detected.
                        flag = 1
                        break
            draw_keypoints(vis, self.tracker.frame_points)

            self.rect_sel.draw(vis)
            cv.imshow('Selected Region', vis)
            cv.waitKey(1)
            if flag == 1:
                print("Dimensions of the book : ", width_of_book)
                return

if __name__ == '__main__':
    print(__doc__)

    import sys
    try:
        img_src = sys.argv[1]
    except:
        img_src = "book_final.jpg"

    Dimensions_width_top = App(img_src).run_original()
    Dimensions_width_bottom = App(img_src).run_original()

    print(Dimensions_width_top)
    print(Dimensions_width_bottom)
    # App(img_src).cv2.setMouseCallback('image',draw_circle)

    # print(Dimensions_cover, [14, 1.1])
    App(img_src).run(Dimensions_width_top, [14, 1.1])
    App(img_src).run(Dimensions_width_bottom, [14, 1.1])
