#!/usr/bin/python3
# This script will decode all .NPY files in the directory
mypath = "/home/milch/predict.Q16/"
# to the tabbed text format

import struct
import numpy as np
import os

def parseNPY(path, fileJustName):
    # load from the file
    inputFile = os.path.join(path, fileJustName + ".npy")
    matrices = np.load(inputFile)

    outputfile = os.path.join(path, fileJustName)
    for m in range(matrices.shape[0]):
        # file name for this matrix
        outFileFull = outputfile + "-" + str(m) + ".txt"
        # output matrix to a numbered file
        np.savetxt(outFileFull, matrices[m], fmt="%i", delimiter="\t")
        


for path, paths, filenames in os.walk(mypath):
    # translate all filenames.
    for filename in filenames:
        fileJustName, fileExtension = os.path.splitext(filename)
        if fileExtension == ".npy":
            print(os.path.join(path, fileJustName))
            parseNPY(path, fileJustName)
