from Net import Net
import Tkinter as tk
import functions
from camera import camera
import glob
import os
import App

try_again_message = '\nUnexpected input.\nTry again\n'

def option_1 (frame, list):   
    "(1) Create net"
    filename, rows, columns, groupSize = list
    try:
        rows = int(rows)
        columns = int(columns)
        groupSize = int(groupSize)
        net = Net(rows, columns, groupSize, filename)
    except (IOError or ValueError):
        raise
    else:
        text = tk.Label(frame, text = '\nNet created on folder: training.\n Filename: ' + filename + '\n')
        text.pack()

def option_2 (frame, list):
    "(2) Read net from file"
    filename, verbose = list
    tab_frame = tk.Frame(frame)
    try:
        net = functions.read_file_net(filename)
    except IOError:
        raise
    else:
        net.print_properties(tab_frame, verbose)

def option_3 (frame, list):   
    "(3) Set net threshold"
    filename, threshold = list
    try:
        threshold = int(threshold)
        net = functions.read_file_net(filename)
    except IOError:
        raise
    net.setThreshold(threshold, frame)

def option_4 (frame, list):   
    "(4) Copy net"
    filename_from, filename_to = list
    try:
        net_from = functions.read_file_net(filename_from)
        net_to = Net(2, 2, 2, filename_to)
        net_to.duplicate(net_from)
    except (IOError or ValueError):
        raise
    else:
        text = tk.Label(frame, text = '\nNet copied on folder: training.\n Filename: ' + filename_to + '\n')
        text.pack()
            
def option_5 (frame, list):
    "(5) Train net with image files"
    net_filename, image_path_folder = list
    mode = 1
    try:
        functions.train_or_test_folder_img_file(net_filename, image_path_folder, mode, frame)
    except IOError:
        raise
    else:
        img_counter = len(glob.glob1(image_path_folder,"*.png"))
        text = tk.Label(frame, text = '\nNet trained with image files from folder: '+ image_path_folder + '.')
        text.pack()
        text = tk.Label(frame, text = str(img_counter) + ' trained nets saved on folder training.\n')
        text.pack()

def option_6 (frame, list):
    "(6) Train net with image files, test before each training"
    net_filename, image_path_folder = list
    mode = 3
    frame.add_scroll_2_frame(frame.results_frame)
    frame.yes_counter = 0
    try:
        functions.train_or_test_folder_img_file(net_filename, image_path_folder, mode, frame)
    except IOError:
        raise
    else:
        text = tk.Label(frame.results_frame, text = '\nNet trained with image files from folder: '+ image_path_folder + '.')
        text.pack()
        text = tk.Label(frame.results_frame, text = str(frame.yes_counter) + ' trained nets saved on folder training.\n')
        text.pack()

def option_7 (frame, list):
    "(7) Train net with image files, test before each training, if test is below the threshold, train with the image"
    net_filename, image_path_folder = list
    mode = 4
    try:
        functions.train_or_test_folder_img_file(net_filename, image_path_folder, mode, frame)
    except IOError:
        raise
    else:
        text = tk.Label(frame.results_frame, text = '\nNet trained with image files from folder: '+ image_path_folder + '.')
        text.pack()
        net_path_folder = '/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition/'
        str_net_files =  net_path_folder + net_filename.split('.')[0] + '*.p'
        net_files = glob.glob(str_net_files)
        text = tk.Label(frame.results_frame, text = str(len(net_files)-1) + ' trained nets saved on folder training.\n')
        text.pack()
        
def option_8 (frame, list):
    "(8) Train net with camera"
    net_filename = list[0]
    try:
        image_path_folder = camera (3, net_filename) + '/'
        functions.train_or_test_folder_img_file(net_filename, image_path_folder, 1)
    except ValueError:
        text = tk.Label(frame, text = '\nImage files saved on folder: '+ image_path_folder + '.')
        text.pack()
        raise
    except IOError:
        raise
    else:
        img_counter = len(glob.glob1(image_path_folder,"*.png"))
        text = tk.Label(frame, text = '\nImage files saved on folder: '+ image_path_folder + '.')
        text.pack()
        text = tk.Label(frame, text = str(img_counter) + ' trained nets saved on folder training.\n')
        text.pack()

def option_9 (frame, list):
    "(9) Train net with camera, test before training"
    net_filename = list[0]
    try:
        camera (5, net_filename, frame)
    except IOError:
        raise
    
def option_10 (frame, list):
    "(10) Test net with image files"
    net_filename, image_path_folder  = list
    frame.add_scroll_2_frame(frame.results_frame)
    try:
        functions.train_or_test_folder_img_file(net_filename, image_path_folder, 2, frame)
    except IOError:
        raise
    
def option_11 (frame, list):
    "(11) Test net with camera"
    net_filename = list[0]
    try:
        camera (2, net_filename, frame)
    except IOError:
        raise

def option_12 (frame, list):
    "(12) Test net with camera and take pictures"
    net_filename = list[0]
    try:
        camera (4, net_filename, frame)
    except IOError:
        raise

def option_13 (list):
    "(13) Debugger"
    filename = 'net_trained_21_times.p'
    filename = filename.split("_")[0]
    filename = filename.split(".")[0]

def train_net_with_img_file (net_filename, image_path_folder, frame,  mode):
    try:
        functions.train_or_test_folder_img_file(net_filename, image_path_folder, mode, frame)
    except IOError:
        raise
    else:
        img_counter = len(glob.glob1(image_path_folder,"*.png"))
        text = tk.Label(frame, text = '\nNet trained with image files from folder: '+ image_path_folder + '.')
        text.pack()
        text = tk.Label(frame, text = str(img_counter) + ' trained nets saved on folder training.\n')
        text.pack()
