from gamera.plugin import *
from gamera.args import *
import _aruspix_plugin

# C++ method
class flatten(PluginFunction):
    """Flatten the image content into a black and white image. Everything
which is not white in the original image is considered as black
"""
    category = "Aruspix"
    self_type = ImageType([GREYSCALE])
    return_type=ImageType([ONEBIT])
    author="Laurent Pugin"

class extract(PluginFunction):
    """Extract on plan of the image. The music staves (black in the pre-classified
image in Aruspix), the border (light grey), ornate letters (dark green), the text
in staff (light green), the lyrics (orange) and the titles (yellow). The image return
is a black and white one with the selected content"""
    category = "Aruspix"
    self_type = ImageType([GREYSCALE])
    return_type=ImageType([ONEBIT])
    args = Args([Choice("Category", ["music staves","borders","ornate letters","in staff text","lyrics","titles"], default=0)])
    author="Laurent Pugin"

class visualize(PluginFunction):
    """Visualize the pre-classified image of the Aruspix file. The different categories
are shown in the corresponding colours, with black for the music staves, light grey for 
the borders, dark green for the ornate letters, and so on...
"""
    category = "Aruspix"
    self_type = ImageType([GREYSCALE])
    return_type=ImageType([RGB])
    author="Laurent Pugin"

class AruspixModule(PluginModule):
    category = None
    cpp_headers=["aruspix_plugin.hpp"]
    functions = [extract, visualize, flatten]
    url = "http://www.aruspix.net"

module = AruspixModule()
