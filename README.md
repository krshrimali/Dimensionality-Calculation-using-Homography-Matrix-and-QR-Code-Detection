# Measurement-of-Book-Cover
OpenCV based dimensional measurement of a book cover using Homography and Ratio comparison.

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

--------------------------------------------------------------------------------
Inspiration Credits: learnopencv.com latest blog post on QR Code Detection.
