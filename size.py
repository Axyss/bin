from tkinter import *
import os

class Size():

    def __init__(self):

        self.sizeVar = "0.0 MB"
        self.totalSize = 0

    def obtainSize(self, videoFiltered):

        for i in videoFiltered:

            self.totalSize += os.path.getsize(i)  # Default unit: byte

            if self.totalSize < 1000000000:  # Check if MB

                self.sizeVar = str(round(self.totalSize / 1000000, 2)) + " MB"

            elif self.totalSize >= 1000000000:  # Check if GB
                self.sizeVar =str(round(self.totalSize / 1000000000, 2)) + " GB"

        return self.sizeVar

size_obj = Size()

