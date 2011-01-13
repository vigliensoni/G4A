
# piece of code that load an aruspix file into a classifier
# file has to have groundtruth loaded in it

from gamera.args import *
from gamera import gamera_xml
from gamera import knn
from gamera.toolkits.aruspix.ax_page import *
from gamera.toolkits.aruspix.ax_file import *

axfile=""
group=0

# start options dialog
dialog=Args([FileOpen("Aruspix file", axfile, "*.axz"),
			 Choice( "group", ["Group","No group"] )],
			name="Select the file")
params=dialog.show()

if params is not None and params[0]:
	# map parameters
	i=0
	axfile=params[i]; i+=1
	group=params[i]; i+=1

f = AxFile(axfile, "")

gl = []
if group == 1:
	gl = gamera_xml.glyphs_from_xml(f.tmpdirname + "gamera_page_no_group.xml")
else:
	gl = gamera_xml.glyphs_from_xml(f.tmpdirname + "gamera_page_group.xml")
image = load_image(f.tmpdirname + "img2.tif")

classifier = knn.kNNInteractive()
classifier.display(gl,image)


