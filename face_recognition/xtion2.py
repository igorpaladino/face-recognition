import numpy
import cv2
import os
import cv2.cv as cv

print cv2.__version__

width = 640
height = 480

obj = cv2.VideoCapture(cv.CV_CAP_OPENNI)
print 'hey'
#obj.set(3,width) #set the frame width
#obj.set(4,height) #set the frame height
print 'hey2'

obj.set(cv.CV_CAP_OPENNI_IMAGE_GENERATOR_OUTPUT_MODE, cv.CV_CAP_OPENNI_VGA_30HZ)

print obj.get(cv.CV_CAP_PROP_OPENNI_REGISTRATION)

if obj.isOpened(): # try to get the first frame
    verification, frame = obj.read() # capture frame from camera
# ret => boolean, if camera reads correctly, ret = True
# frame => a single picture RGB matrix (array of arrays of arrays), dimmension width x heigth x 3 
    print 'hey3'

else:
    verification = False
    print 'hey4'

cv2.namedWindow('preview')
print 'hey5'

cv2.moveWindow('preview', 320, 0)
print 'hey6'

os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''') # bring camera to the front
print 'hey7'

while verification:
    print 'hey8'
    gray_frame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
    # gray => gray scale matrix width x heigh
        
    gray_frame = numpy.fliplr(gray_frame)
    # flip matrix left to right in order to get video more intuitive
    gray_frame = numpy.array(gray_frame)

    cv2.imshow('preview',gray_frame)
    verification, frame = obj.read() # capture frame from camera
    key = cv2.waitKey(20)

    if key == 27: # exit on ESC
        quit(obj)
    print 'hey7'

def quit(obj):
    pygame.mixer.quit()
    obj.release()
    cv2.destroyAllWindows()
