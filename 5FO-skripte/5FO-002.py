#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path
import datetime

# specific
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


"""
This script takes raw extracted features as input.  
Input is one or several CSV file(s) with image features.
Output is one CSV file with merged and optionally normalized features.
"""


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "4FE-daten", "4FE-003.csv")
targetdatafile = join(workdir, "6FO-daten", "6FO-002.csv")
docfile = join(workdir, "6FO-daten", "6FO-002.txt")


# ===============================
# Functions
# ===============================


def load_data(sourcedatafile): 
	"""
	Load the CSV file as a pandas DataFrame.
	"""
	with open(sourcedatafile, "r") as infile: 
		data = pd.DataFrame.from_csv(infile, sep=";")
		return data


def normalize_data(data): 
	"""
	Perform a column-wise z-score transformation.
	This is applied to the columns listed below.
	"""
	for column in ["histmax", "histmed", "histstd"]: 
		data[column] = (data[column] - np.mean(data[column])) / np.std(data[column])
	return data


def save_data(data, targetdatafile):
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=";")


# ===============================
# Documentation functions
# ===============================


def get_timestamp(): 
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp

def read_previous_docfile():
    prevdocdict = {}
    with open(os.path.splitext(sourcedatafile)[0] + ".txt", "r") as prev:
        lines = (line.strip().partition(' = ') for line in prev)
        for cat, sep, con in lines:
            if sep:
                prevdocdict[cat] = con
    return prevdocdict

def write_docfile(sourcedatafile, targetdatafile, docfile):
    prevdoc = read_previous_docfile()
    operations = "operations = apply a z-score transformation to each histogram value." + " // " + prevdoc['operations']
    sourcestring = "sourcedata = " + str(os.path.basename(sourcedatafile)) + " // " + prevdoc['sourcedata']
    targetstring = "targetdata = " + str(os.path.basename(targetdatafile)) + " // " + prevdoc['targetdata']
    scriptstring = "script = " + str(os.path.basename(__file__)) + " // " + prevdoc['script']
    sizestring = "size = " + prevdoc['size']
    commentstring = "comment = " + prevdoc['comment']
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==5FO==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + \
              sizestring + "\n" + commentstring + "\n" + timestamp + "\n"
    with open(docfile, "w") as outfile:
        outfile.write(doctext)
		


# ========================
# Main
# ========================

def main(sourcedatafile, targetdatafile, docfile):
    data = load_data(sourcedatafile)
    data = normalize_data(data)
    save_data(data, targetdatafile)
    write_docfile(sourcedatafile, targetdatafile, docfile)
        
main(sourcedatafile, targetdatafile, docfile)
