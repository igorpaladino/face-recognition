import cv2
import numpy as numpy

width = 64
height = 64

drawing = numpy.zeros((height,width), numpy.uint8)

face_width = (height-1)/1.618
a1 = ((width-1) - face_width)/2
a2 = int(a1 + face_width)
a1 = int(a1)

point1 = (a1, 0)
point2 = (a2, height-1)

cv2.rectangle(drawing, point1, point2, 255)
cv2.imshow("drawing", drawing)
cv2.waitKey()
cv2.destroyAllWindows()