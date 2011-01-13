# piece of code that load an aruspix file into a classifier
# file has to have groundtruth loaded in it

import sys
import time
import threading

from gamera.core import *
from gamera.config import config
from gamera import gamera_xml
from gamera import knn




init_gamera()

config.set("progress_bar",True)

infile=sys.argv[1]
outfile=sys.argv[2]
time_factor=sys.argv[3]

iknn=knn.kNNInteractive([],['aspect_ratio','moments', 'nrows_feature','ncols_feature', 'volume64regions'],0)
iknn.num_k = 3
iknn.from_xml_filename(infile)
nknn = iknn.noninteractive_copy()

def hello():
	global nknn
	global outfile
	global infile
	nknn.stop_optimizing()
	print "OPT", infile, "GA initial", nknn.ga_initial,"GA best", nknn.ga_best, "GA generation", nknn.ga_generation
	nknn.save_settings(outfile)
	

nknn.start_optimizing()

t = threading.Timer(int(time_factor) * 20 * 60.0, hello)
t.start() # after 30 seconds, "hello, world" will be printed