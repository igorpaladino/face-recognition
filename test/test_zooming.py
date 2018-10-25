obj = cv2.VideoCapture(0)

small = cv2.resize(image, (0,0), fx=0.5, fy=0.5)


if obj.isOpened(): # try to get the first frame
    verification, frame = obj.read() # capture frame from camera
# ret => boolean, if camera reads correctly, ret = True
# frame => a single picture RGB matrix (array of arrays of arrays), dimmension width x heigth x 3
else:
    verification = False

while verification:
    
    gray_frame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
    # gray => gray scale matrix width x heigh
    
    gray_frame = numpy.fliplr(gray_frame)
    # flip matrix left to right in order to get video more intuitive
    
    gray_frame = numpy.array(gray_frame)
    cv2.rectangle(gray_frame, point1, point2, 255)
    # draw an rectangle
    
    cv2.namedWindow('preview')
    cv2.namedWindow('picture')
    
    gray_frame = cv2.resize(gray_frame, (0,0), fx=0.5, fy=0.5)
    
    cv2.imshow('preview',gray_frame)
    verification, frame = obj.read() # capture frame from camera
    key = cv2.waitKey(20)
    
    if key == 13: # take a snapshot on ENTER
        sound.play()
        filename = newpath + '/' + 'picture'+ str(num_picture) +'.png'
        cv2.imwrite(filename, gray_frame) # write the image
        num_picture+=1
    elif key == 27: # exit on ESC
        obj.release()
        cv2.destroyAllWindows()
    break