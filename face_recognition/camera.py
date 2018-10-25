import functions
from MyImage import MyImage
import pygame #used for the sound
import os
import time
import numpy
import cv2

def camera(mode, net_filename = None, window_frame=None):
    """
    Input = ( mode, net filen name, Frame)
    mode 1: camera take pictures when ENTER is pressed and save it on files on folder images
    mode 2: camera take pictures and test them on the net file passed, the output of the net is print
    mode 3: camera take burst pictures till ESC is pressed and save it on files on folder images    
    mode 4: camera take pictures and test them on the net file passed, the output of the net is print, pictures are taken when ENTER is pressed
    mode 5: camera take one picture when ENTER is pressed, test it on the net, show the results and ask the user if he/she wants to train the net with the picture
    """

    #read net file if it was passed
    if net_filename:
        try:
            net = functions.read_file_net(net_filename)
        except IOError:
            raise

    width = 640
    height = 480
 
    obj = cv2.VideoCapture(0)
    obj.set(3,width) #set the frame width
    obj.set(4,height) #set the frame height
    
    num_picture = 1
    
    # setting values for the rectangle drawing
    point1 = (170, 20)
    point2 = (469, 459)
    
    #oval face
    oval_face = cv2.imread('oval_face.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    inv_oval_face = cv2.imread('inv_oval_face.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    
    # setting the shutter click sound
    pygame.mixer.init()
    sound = pygame.mixer.Sound("/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition/shutter_click.wav")

    if obj.isOpened(): # try to get the first frame
        verification, frame = obj.read() # capture frame from camera
    # ret => boolean, if camera reads correctly, ret = True
    # frame => a single picture RGB matrix (array of arrays of arrays), dimmension width x heigth x 3 

    else:
        verification = False
    
    cv2.namedWindow('preview')
    cv2.moveWindow('preview', 320, 0)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''') # bring camera to the front
    
    start = time.time()
    first_shot = True
    createDir = False
    newpath = None
    
    while verification:
        gray_frame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
        # gray => gray scale matrix width x heigh
        
        gray_frame = numpy.fliplr(gray_frame)
        # flip matrix left to right in order to get video more intuitive
        gray_frame = numpy.array(gray_frame)
                
        gray_frame_oval = cv2.addWeighted(gray_frame,1,oval_face,1,0)
        # draw an oval face
                
        if mode == 5:
            gray_frame_oval_copy = numpy.copy(gray_frame_oval)
            # copy the frame

        if mode == 1 or mode == 5:
            cv2.putText(gray_frame_oval, "Press OK to take a photo", (0,469), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8, 0)        
            # put message if in mode 1 or 5
        
        cv2.imshow('preview',gray_frame_oval)
        verification, frame = obj.read() # capture frame from camera
        key = cv2.waitKey(20)
        
        gray_frame = cv2.addWeighted(gray_frame,1,inv_oval_face,1,0)

        gray_frame = gray_frame[20:459, 170:469]
        # crop just the rectangle (face)
        
        gray_frame = cv2.resize(gray_frame, (0,0), fx=(3.0/20), fy=(3.0/20))
        # resize for a picture 66p x 45p
        
        # mode take pics
        if mode==1:
            if key == 13: # take a snapshot on ENTER
                if num_picture == 1:
                    newpath = create_new_path()
                num_picture = take_pics(gray_frame, num_picture, sound, newpath)
                            
        # mode log in
        elif mode==2:
            log_in(gray_frame, net, window_frame, obj)
        
        # mode multi_shot or mode log in + take pics
        elif ( mode==3 ) and ( time.time() > start + 1 ): 
            if num_picture == 1 and createDir == False:
                newpath = create_new_path()
                createDir = True
            if time.time() > start + 5:
                first_shot = False
            if first_shot:
                pass
            else:
                num_picture = take_pics(gray_frame, num_picture, sound, newpath)
                start = time.time()
        
        if ( mode==4 or mode==5 ):
            log_in(gray_frame, net, window_frame, obj)
            if key == 13: # take a snapshot on ENTER
                if num_picture == 1:
                    newpath = create_new_path()
                num_picture = take_pics(gray_frame, num_picture, sound, newpath)
                if mode == 5:
                    cv2.putText(gray_frame_oval_copy, "Press OK to train photo", (0,454), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8, 0)        
                    cv2.putText(gray_frame_oval_copy, "Or any other key not to", (0,474), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8, 0)        
                    cv2.imshow('preview',gray_frame_oval_copy)                    
                    log_in(gray_frame, net, window_frame, obj)
                    key_2 = cv2.waitKey(0) #wait for a key
                    if key_2 == 13:
                        myImage  = MyImage(gray_frame, 2)
                        functions.train(net, myImage)
                    else:
                        filename = newpath + '/' + 'picture'+ str(num_picture-1).zfill(4) +'.png'
                        os.remove(filename)
            
        if key == 27: # exit on ESC
            quit(obj)
            return newpath

def quit(obj):
    pygame.mixer.quit()
    obj.release()
    cv2.destroyAllWindows()

def create_new_path():
    """
    Creates an empty folder on folder images to hold the image files
    folder name is pack followed by a number, ex.: pack1
    """
    # creating folder
    index = 1
    createDir = False
    while not createDir:
        newpath = ((r'images/new/pack%s') %(str(index).zfill(2)))
        if os.path.exists(newpath):
            index+=1
        else:
            os.makedirs(newpath)
            createDir = True
    return newpath

def take_pics(gray_frame, num_picture, sound, newpath):
    """
    Input = ( image matrix  frame, picture number, path to save images )
    take pictues and saves them on the path passed as argument
    """
    sound.play()
    filename = newpath + '/' + 'picture'+ str(num_picture).zfill(4) +'.png'
    cv2.imwrite(filename, gray_frame) # write the image
    num_picture+=1
    return num_picture

def log_in(gray_frame, net, window_frame, obj):
    """
    Input = ( image matrix frame, net file, window frame )
    camera take pictures and test them on the net file passed, the output ou the net is print
    """
    mode = 2 # indicates it reads from camera
    myImage  = MyImage(gray_frame, 2)
    try:
        functions.test(net, myImage, mode, window_frame)
    except ValueError:
        quit(obj)
        raise