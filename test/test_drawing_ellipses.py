import cv2
import numpy
import time

width = 640
height = 480

drawing = numpy.zeros((height,width), numpy.uint8)
#drawing.fill(255)
#create a black image

centre = (width/2,height/2)

if height%2 == 0:
    radius2 = height/2 - 1
else:
    radius2 = height/2
radius1 = int(radius2/1.618)

axes = (radius1, radius2)

cv2.ellipse (drawing, centre, axes, 0, 0, 360, 255)

#cv2.namedWindow('preview')

cv2.imshow('preview',drawing)
cv2.waitKey()
cv2.destroyAllWindows()