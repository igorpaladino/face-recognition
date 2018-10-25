import sys
sys.path.append(r'/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition')
from Net import Net
from MyImage import MyImage
import numpy
import glob
import os
import functions
import math
import matplotlib.pyplot as plt
import natsort

#INPUT
net_path_folder = '/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/report/figures/experiment_16/nets'

ones_list = []
net_files = glob.glob(os.path.join(net_path_folder, '*.p'))
net_files = natsort.natsorted(net_files, key=lambda y: y.lower())
net = functions.read_file_net(net_files[0])
memory_size = net.numFunctions*math.factorial(net.groupSize)

for filename in net_files:
    net = functions.read_file_net(filename)
    ones_list.insert(net.trained_times,net.ones)

ones_list = numpy.array(ones_list)
percent_ones_list = ones_list/(float(net.numFunctions*math.factorial(net.groupSize)))*100

plt.subplot(2, 1, 1)
plt.stem(ones_list)
plt.title('Population of ones in memory')
plt.ylabel('number of ones in MEM')

plt.subplot(2, 1, 2)
plt.stem(percent_ones_list)
plt.xlabel('number of trainings')
plt.ylabel('number of ones in MEM (%)')

net_id = net.filename.split(".p")[0]
net_id = net_id.split("/")[-1]
net_id = net_id.split("_")[0]
png_filename = "ones_" + net_id

plt.savefig( png_filename )
#plt.show()