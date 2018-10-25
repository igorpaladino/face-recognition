import sys
sys.path.append(r'/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition')
from Net import Net
from MyImage import MyImage
import glob
import os
import functions
import matplotlib.pyplot as plt
import numpy

#INPUTS
number_image_paths = 2
mode = 1 # mode == 1 if there is no frequency, mode == 2 otherwise
image_path_pattern_trained = '/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/report/figures/experiment_33/testing_pass'
image_path_different_pattern = '/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/report/figures/experiment_33/testing_not_pass'
net_path_folder = '/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition/training'

image_paths = []
image_paths.append(image_path_pattern_trained)
image_paths.append(image_path_different_pattern)

net_files = glob.glob(os.path.join(net_path_folder, '*.p'))

colour = ['b', 'r']

if number_image_paths == 1:
    legend= ['pattern trained']
elif number_image_paths == 2:
    legend= ['pattern trained', 'different patern']

for net_filename in net_files:
        
    net = functions.read_file_net(net_filename)
    net_id = net.filename.split(".p")[0]
    net_id = net_id.split("/")[-1]
    net_id = net_id.split("_")[0]
 
    for image_path in range(number_image_paths):
        
        image_path_folder = image_paths[image_path]
        png_files = glob.glob(os.path.join(image_path_folder, '*.png'))
        summation_list = []
        for filename in png_files:
            myImage  = MyImage(filename)
            summation = functions.train_or_test(net,myImage, 2, 0)
            summation_list.append(summation)
        
        summation_list = numpy.array(summation_list)
        if  mode == 1:
            percent_summation_list = summation_list*100.0/net.numFunctions
        elif  mode == 2:
            percent_summation_list = summation_list
        
        markerline = plt.stem(range(1,len(png_files)+1), percent_summation_list, colour[image_path])
        plt.setp(markerline, 'markerfacecolor', colour[image_path])
        plt.title( net_id + ' tested on unseen images')
        plt.xlabel('picture number')
        if  mode == 1:
            plt.ylabel('net response output (%)')
        elif  mode == 2:
            plt.ylabel('net response output')
        plt.grid(True)
        plt.hold(True)
    
    plt.legend(legend) 
    #plt.show()
    png_filename = net_id + "_tested.png"
    #png_filename = net_id + "_tested_on_same_class.png"
    #png_filename = net_id + "_tested_on_different_class.png"
    plt.savefig( png_filename )
    plt.clf()