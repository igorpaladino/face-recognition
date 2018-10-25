from PIL import Image
import numpy

class MyImage:
    """
    This is a class for the Images that are going to be used in training or reading the nets
    mode 1: read image from a file
    mode 2: read image from matrix
    """
    def __init__(self, filename_or_matrix, mode=1):
        if mode ==1:
            filename = filename_or_matrix
            self.filename = filename
            self.file = Image.open(filename)
            self.rows = self.file.size[1]
            self.columns = self.file.size[0]
            self.numPixels = self.rows * self.columns
            self.matrix = self.convImg2gMatrix()
        elif mode ==2:
            matrix = filename_or_matrix
            self.rows = len(matrix)
            self.columns = len(matrix[0])
            self.numPixels = self.rows * self.columns
            self.matrix = matrix
    
    def convImg2gMatrix(self):
        """
        Convert a Image object to a gray scale matrix
        Input = InputImage object"
        Return this matrix
        """
        self.file = self.file.convert("L")
        matrix = numpy.asarray(self.file)
        # convert image to gray scale image
        # in the array, 0 represents black
        # 255 represents white
        # array[a,b] => a represents the line, b represents the columns
        # array[0,0] is the pixel in the top-left hand corner
        return matrix
