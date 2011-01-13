
# piece of code that load an aruspix file into a classifier
# file has to have groundtruth loaded in it

import os
from gamera.args import *
from gamera import gamera_xml
from gamera import knn

dirname = ""
output = ""

# start options dialog
dialog=Args([Directory("Directory", ""),
			 FileSave( "Output file", "", "*.xml" )],
			name="Directory and output file")
params=dialog.show()

if params is not None and params[0]:
	# map parameters
	i=0
	dirname=params[i]; i+=1
	output=params[i]; i+=1
	
if os.path.exists(output) == True:
	os.remove(output)

classifier = knn.kNNInteractive()
classifier.clear_glyphs()

rseqn = list(os.listdir(dirname))

for filename in rseqn:
	(root, ext) = os.path.splitext(filename)
	if ext in set(['.xml']) and not root.startswith(".") and filename != output:
		classifier.merge_from_xml_filename(os.path.join(dirname,filename))
		
classifier.to_xml_filename(output,False)
