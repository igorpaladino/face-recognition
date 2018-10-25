from Net import Net
from MyImage import MyImage
from math import factorial
import cPickle
import Tkinter as tk
import os
import glob
import App

def rank_order_comp (array, sorted_array):
    """
        Generate a number corresponding to the rank order of the array
        Input  = (array to be ranked, decreasing ordered array)
        Return the rank order (recursive function)
        """
    length = len(array)
    if length == 1:
        return 1
    else:
        element = sorted_array[0]
        parc_rank = array.index(element)*factorial(length-1)
        sorted_array = sorted_array[1:]
        array.remove(element)
        return parc_rank + rank_order_comp(array,sorted_array)
    # for example, in a array [A,B,C], if A>=B>=C, rank=1
    # if A>=C>=B, rank=2
    # if B>=A>=C, rank=3 and so on
    # algorithm calculate smallest rank order if there is a repeated number in the array


def checkCompatibility(net,myImage):
    """
        Check if rows and columns of Net and MyImage are the same, respectvely
        If not raise error
        Input = (Net object, MyImage object)
        """
    try:
        if net.rows != myImage.rows:
            raise ValueError("Number of net rows is different from image rows")
        elif net.columns != myImage.columns:
            raise ValueError("Number of net columns is different from image columns")
    except ValueError:
        raise


def train(net, myImage):
    """
        Train the net using the myImage
        Input = (Net, myImage)
        Give back the memory of the functions populated in the Net
        Saves the net's atributes in a file
        """
    _ = 0
    try:
        train_or_test(net,myImage, 1, _)
    except ValueError:
        raise
    else:
        net.count_ones()
        net.trained_times += 1
        filename = net.filename.split(".")[0]
        filename = filename.split("_trained_")[0]
        filename = filename + '_trained_' + (str(net.trained_times)) + '_times.p'
        file_opened = open(filename,'wb')
        cPickle.dump(net.__dict__,file_opened,2)
        file_opened.close()

def test(net, myImage, mode, frame):
    """
        Test the net using the myImage
        Input = (Net, myImage, mode, Frame)
        Print [ net threshold, output summation, output (True or False) ]
        True, if the pattern was recognized, output summation >= threshold
        False if it was not recognized
        mode = 1: testing with images files
        mode = 2: testing with camera
        mode = 3: testing with images files, wait for a response
        mode = 4: testing with images files, train if output = True
        """
    try:
        summation = 0
        summation = train_or_test(net,myImage, 2, summation)
    except ValueError:
        raise
    else:
        output = False
        if summation >= net.threshold:
            output = True

        if mode==4:
            if not output:
                train(net, myImage)
        else:
            frame.display_test(net, summation, output, mode, myImage)
        
def train_or_test(net, myImage, mode, summation):
    """
        Implements the train and test algorithm as they are really similar
        It was used instead of two functions because it leads to less duplications of code
        There is a biffurcation in the algorithm to implement the different parts of the
        functions train and test ( mode variable implements it )
        Input = ( Net, myImage, bifurcation, summation )
        summation is used in the test_net function, but is a dummy variable in the train_net
        function
        mode = 1: train mode
        mode = 2: test mode
        """
    try:
        checkCompatibility(net,myImage)
    except ValueError:
        raise
    else:
        numFunction = 0
        for function in net.functions:
            group_read = []
            for pixel in function:
                row = pixel/myImage.columns
                column = pixel%myImage.columns
                group_read.append(myImage.matrix[row][column])            
            sorted_group_read = sorted(group_read, reverse=True)
            rank_order = rank_order_comp(group_read,sorted_group_read)
            
            if mode == 1:
                net.memory[numFunction][rank_order-1] = 1
                #if net.frequencies[numFunction][rank_order-1] < 255:
                #    net.frequencies[numFunction][rank_order-1] += 1
                
            else:
                if net.memory[numFunction][rank_order-1] == 1:
                    summation += 1
                    #summation += net.frequencies[numFunction][rank_order-1]
            numFunction+=1
        return summation

def read_file_net(filename):
    """
        Reads a file coinatining the net's attributes
        Input = filename
        Output = net reada and updated
        """
    try:
        file_opened = open(filename,'rb')
    except IOError:
        raise IOError("File: " +  filename + " does not exist.")
    else:
        file_opened = open(filename,'rb')
        tmp_dict = cPickle.load(file_opened)
        file_opened.close()
        net = Net(2,2,2,'training/temp.p')
        os.remove('/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition/training/temp.p')
        net.__dict__.update(tmp_dict)
        net.filename = filename
        return net

def train_or_test_folder_img_file (net_filename, image_path_folder, mode, frame=None):
    """
    Implements the train and test algorithm as they are really similar on folder images
    Input = ( Net, image file, mode: train or test, Frame (used just in test mode) )
    mode = 1: train mode
    mode = 2: teste mode
    mode = 3: train mode, but test each image and wait for user response to train it or not
    mode = 4: train mode, but test each image and train it only if its response is above threshold
    """
    
    try:
        net = read_file_net(net_filename)
    except IOError:
        raise
    else:
        png_files = glob.glob(os.path.join(image_path_folder, '*.png'))
        if not png_files:
            raise IOError("Image path folder does not exist.")
        net = read_file_net(net_filename)
        for filename in png_files:
            myImage  = MyImage(filename)
            try:
                if mode == 1:
                    train (net, myImage)
                elif mode == 2:
                    test (net, myImage, 1, frame)
                elif mode == 3:
                    test (net, myImage, 3, frame)          
                elif mode == 4:
                    test (net, myImage, 4, frame)          
            except ValueError:
                raise