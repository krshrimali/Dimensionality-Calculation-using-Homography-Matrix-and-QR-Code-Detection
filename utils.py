'''
Utility functions for "Measurement of book cover" Project.
Available functions:
1) Euclidean Distance Function
2) Average Calculation
3) Mouse Handling, (Left Button Clicked Once)
4) Get four points from the user
'''
import math
import cv2
import numpy as np

def distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

def avg(x, y):
    return (x + y)/2.0

def mouse_handler(event, x, y, flags, data) :
    if event == cv2.EVENT_LBUTTONDOWN :
        cv2.circle(data['im'], (x,y), 3, (0,0,255), 1, 1);
        cv2.imshow("Image", data['im']);
        if len(data['points']) < 4 :
            data['points'].append([x,y])

def get_four_points(im):

    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []

    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)

    return points