# Measurement-of-Book-Cover
OpenCV based dimensional measurement of a book cover using Homography and Ratio comparison.

## Files Description 

1) `book_dimensions.py` : Simpler, easy and gives lengths of all edges.
2) `book_dimension_detection.py` : Complex and gives only width and height of the book.
3) `book_dimension_top_bottom_edge.py` : Complex, gives length of top and bottom edge of the book (only width)

Folder: `images/` : All output and input images are in this folder. Use `book_final.jpg` as sample image. 

Documentation of each file is in the code itself.

## What it does?
Approximation of the dimensions of a cover page of a book using techniques: Homography Algorithms, [QR Code Detection using Zbar]

## How it does?
1) QR Code generation using any online web service. [Example: https://www.qr-code-generator.com/]

2) Detection of the QR Code and Text generation [encoded in the QR code - assuming text or any hyperlink etc.] using zbar module in Python.
Credits: learnopencv.com 

3) Printing out the QR Code on a page, assuming it to be on a book - take the snap of it, and determine the approximate dimensions
of the book cover, using the measured (manually) dimensions of the QR code.

Note: The QR Code detection has been shown in qr_code_detection.py file, although in the book dimension code - a text has been assumed
instead of QR code because of some unavailability of the printing facilities. The version for QR code will be out soon.

4) Homography technique is used, feature detection, choosing the image of the QR code as the selected area.

## Challenges

1) What if a stack of several books is there and then the snap is clicked? [Challenge credits: Vishwesh Ravi Shrimali].

2) Which angle should the snap be taken? Sideways? Which one is the better?

3) Can we measure the number of books in the stack based on the photo angle?

## Debugging 

In case of errors, import exceptions for following libraries:

1) video : No module named "video"

Copy and paste video.py from [Video Module: OpenCV](https://github.com/opencv/opencv/blob/master/samples/python/video.py) to the current directory.

2) plane\_tracker: No module named 'plane\_tracker'

Copy and paste plane\_tracker.py from [Plane Tracker: OpenCV](https://github.com/opencv/opencv/blob/master/samples/python/plane_tracker.py) to the current directory.

3) common : No module named 'common' 

Copy and paste common.py from [Common Module: OpenCV](https://github.com/opencv/opencv/blob/master/samples/python/common.py) to the current directory.

4) numpy : No module named 'numpy'

Install numpy either using pip or build from source. `pip install numpy` [or `pip3` based on the pip and python versions] should do, if not, please follow the searches on google.

5) cv2 : No module named 'cv2'

You need to install OpenCV2 then. `pip install opencv-python` should do, or follow searches from google for more information.

Note: No function `ORB_create()` [most probably when you are using python3.5(+) version], if this error comes, then replace `ORB_create(nfeatures = 1000)` with `ORB(nfeatures = 1000)` in `plane_tracker.py` file.

--------------------------------------------------------------------------------
Inspiration Credits: learnopencv.com latest blog post on QR Code Detection.
