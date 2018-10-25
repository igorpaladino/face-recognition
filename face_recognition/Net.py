from random import choice
from math import factorial
from bitarray import bitarray
import Tkinter as tk
import cPickle
import numpy as np
import copy
import math

class Net:
    """
    This is a class that generates single nets. This net can be trainned or read.
    Parameters: functions (the random groups), memory
    """
    def __init__(self, rows, columns, groupSize, filename):
        self.rows = rows
        self.columns = columns
        self.groupSize = groupSize
        self.numFunctions = self.rows*self.columns/self.groupSize
        self.functions = self.genRandomGroups()
        #self.functions = self.genHorizGroups()
        #self.functions = self.genVertGroups()
        #self.functions = self.genBlockGroups()
        self.memory = self.generate_mem()
        self.threshold = self.numFunctions
        self.trained_times = 0
        self.filename = '/Users/igorpgcosta/Documents/Aptana Studio 3 Workspace/face_recognition/' + filename
        self.ones = 0
        self.save()
        #self.frequencies = np.zeros((self.numFunctions, (factorial(self.groupSize))), dtype=np.uint8 )
        # threshold starts at value equal the number of functions (AND function)
    
    def generate_mem(self):
        """
        Generate a matrix for the memory of the functios
        Each row is the memory of a function
        Input = (Net)
        Return the memory of the functions
        """

        memFunctions = []
        for _ in range (self.numFunctions):
            memFunction = bitarray(factorial(self.groupSize))
            memFunction.setall(False)
            memFunctions.append(memFunction)

        return memFunctions
    
    def genRandomGroups(self):
        """
        Generate the pixel groups randomly for the functions of the digital network
        Input = (Net)
        Return a list where each component of the list is a array containing a pixel group
        """
        groupList =[]
        pixels = range(0,self.rows*self.columns)
        for _ in range (self.numFunctions):
            group = []
            for aux in range(0,self.groupSize):
                element = choice(pixels)
                group.append(element)
                pixels.remove(element)
            groupList.append(group)
        return groupList

    def genHorizGroups(self):
        """
        Generate the pixel groups horizontally for the functions of the digital network
        Input = (Net)
        Return a list where each component of the list is a array containing a pixel group
        """
        groupList =[]
        for aux in range (self.numFunctions):
            group = range ( 0 + self.groupSize*aux, self.groupSize*(aux + 1) )
            groupList.append(group)
        return groupList

    def genVertGroups(self):
        """
        Generate the pixel groups vertically for the functions of the digital network
        Input = (Net)
        Return a list where each component of the list is a array containing a pixel group
        """
        list =[]
        for aux in range (self.columns):
            group_list = range ( 0 + aux, self.rows*self.columns, self.columns)
            for element in group_list:
                list.append(element)

        groupList =[]
        for aux in range(self.numFunctions):
            group = list[ 0 + aux*self.groupSize : self.groupSize*(aux + 1)]
            groupList.append(group)
        
        return groupList

    def genBlockGroups(self):
        """
        Generate the pixel groups by blocks for the functions of the digital network
        Input = (Net)
        Return a list where each component of the list is a array containing a pixel group
        """
        
        try:
 
            byRow = byColumn = int(math.sqrt(self.groupSize))
            groupByRow = []            
 
            for row in range (self.rows):
                list = []
                for aux in range(self.columns/byColumn):
                    list.append(range( aux*byColumn + row*self.columns, byColumn*(aux + 1) + row*self.columns))
                groupByRow.append(list)            
            
            groupList = []
            
            for v_aux in range (self.rows/byRow):
                for aux in range (self.columns/byColumn):
                    list = []
                    for index in range(byRow):        
                        list.extend(groupByRow[v_aux*byRow+index][aux])
                    groupList.append(list)
            return groupList
        except ValueError:
            raise ValueError("group size must be a perfect square")

    
    def setThreshold(self, newThreshold, frame):
        """
        Change threshold to newThreshold input
        Input = ( Net, new threshold value, frame )
        Print a message saying the threshold was changed
        """
        self.threshold = newThreshold
        text = tk.Label(frame, text = '\nThreshold was set to %i\n' %newThreshold)
        text.pack()
        self.save()
    
    def save(self):
        """
        Creates a file with the object atributes (the net)
        Input = Net
        """
        file_opened = open(self.filename,'wb')
        cPickle.dump(self.__dict__,file_opened,2)
        file_opened.close()
    
    def count_ones(self):
        """
        Count number of ones in the whole memory
        Changes the property self.ones to this value
        Input = Net
        """
        self.ones = 0
        for memory_function in self.memory:
            self.ones += memory_function.count(1)
    
    def print_properties(self, frame, verbose = None):
        """
        Print properties of the net in the window
        Input = ( Net, Frame, Verbose )
        If verbose == 1, the number or ones and the frequencies are also print 
        """     
           
        headers = ['property name', 'property value']
        properties = [['ones in memory', '%.2f' %(self.ones/float(self.numFunctions*factorial(self.groupSize))*100) + ' %'],['rows', str(self.rows)], ['columns', str(self.columns)], ['group size', str(self.groupSize)], ['num of functions', str(self.numFunctions)], ['threshold', str(self.threshold)], ['times trained', str(self.trained_times)]]
        
        tk.Label(frame, text = '').grid(row=0, column = 0)
        tk.Label(frame, text = '').grid(row=0, column = 1)
        
        column = 0
        for text in headers:
            tk.Label(frame, text = text).grid(row=1, column = column)
            column+=1
        
        row = 2
        for tuple_text in properties:
            tk.Label(frame, text = tuple_text[0]).grid(row=row, column = 0)
            tk.Label(frame, text = tuple_text[1]).grid(row=row, column = 1)
            row+=1

        tk.Label(frame, text = '').grid(row=row, column = 0)
        tk.Label(frame, text = '').grid(row=row, column = 1)
        
        if verbose == 1:
            tk.Label(frame, text = 'ones:').grid(row=row, column = 0)
            tk.Label(frame, text = self.ones).grid(row=row, column = 1)
            row+=1
            tk.Label(frame, text = 'functions:').grid(row=row, column = 0)
            tk.Label(frame, text=self.functions).grid(row=row, column = 1)
            #row+=1
            #tk.Label(frame, text = 'memory:').grid(row=row, column = 0)
            #tk.Label(frame, text=self.memory).grid(row=row, column = 1)
            #row+=1
            #np.set_printoptions(threshold=np.nan)
            #tk.Label(frame, text = 'frequencies:').grid(row=row, column = 0)
            #tk.Label(frame, text=self.frequencies).grid(row=row, column = 1)
        frame.pack()
        
    def duplicate (self, net_from):
        """
        Copy just the structure of the net ( functions, for example )
        memory of the net is let empty
        """ 
        self.rows = net_from.rows
        self.columns = net_from.columns
        self.groupSize = net_from.groupSize
        self.numFunctions = net_from.numFunctions
        self.functions = np.copy(net_from.functions)
        self.memory = self.generate_mem()
        self.threshold = net_from.threshold
        self.trained_times = 0
        self.ones = 0
        #self.frequencies = np.copy(net_from.frequencies)
        self.save()