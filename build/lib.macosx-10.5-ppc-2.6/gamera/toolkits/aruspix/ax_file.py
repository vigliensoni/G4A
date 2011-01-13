# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

##############################################################################
# ax_file.py
#
# 2008-01-15
#
##############################################################################

from gamera.core import *

import zipfile
import os
import warnings

# LP rough adaptation from otr_staff.py, leave you check what is needed...
class AxFile:
##############################################################################
    """Manipulates an Aruspix file and stores its information.
    
An object of this class provides the following functionality:

- Read (unzip) the file
- Write (zip) the file

.. note:: 

A *AxFile* object has several public properties, that can be manipulated by
the user. The following table gives a detailed view on this.

+-----------------------+---------------------------------------------------+
| TODO  	      		| TODO								                |
+-----------------------+---------------------------------------------------+


.. _constructor: gamera.toolkits.aruspix.ax_page.AxFile.html#init

:Author: Laurent Pugin and Jason Hockman
"""

    ######################################################################
    # constructor
	#
	# 2008-01-16
    # 
    def __init__(self, filename, tmpdir):
        """Constructs and returns a *AxFile* object.

Signature:

  ``__init__(filename, tmpdir)``

with

  *filename*:
    The name of the Aruspix file to be opened.

  *tmpdir*:
    The directory where to extract the file content.
"""
		self.filename = filename
		self.tmpdir = tmpdir
		self.deletedir = False
		if self.tmpdir == "":
			self.tmpdir = os.tmpnam()
			self.deletedir = True
			os.mkdir(self.tmpdir)
		#print self.tmpdir
		#print self.filename
		self.tmpdirname = self.tmpdir + str(os.path.normcase('/'))
		zip = zipfile.ZipFile(self.filename, 'r') 
        for name in zip.namelist():
			#print self.tmpdir + str(os.path.normcase('/')) + name
			file(self.tmpdirname + name, 'wb').write(zip.read(name))
			
		# some basic verifications
		if os.path.exists(self.tmpdirname + "img0.tif") == False \
			or os.path.exists(self.tmpdirname + "img1.tif") == False \
			or os.path.exists(self.tmpdirname + "index.xml") == False:
			warnings.warn("The minimal content of the Aruspix file seems to be missing")


    ######################################################################
    # destructor
	#
	# 2008-01-20
    #
    def __del__(self):
        """Delete tmpdir if necessary. Does not recursively delete the directory, will fail
if subdirectories are included

Signature:

  ``__del__()``
"""
		if self.deletedir == True:
			for name in os.listdir(self.tmpdir):
				# print self.tmpdir + str(os.path.normcase('/')) + name
				os.remove(self.tmpdirname + name)
			os.rmdir(self.tmpdir)
			
			
    ######################################################################
    # save( filename = "" )
    #
    # 2008-01-15 
    #		
   	def save(self, filename = "" ):
		"""Save the Aruspix file.

Signature:

  ``save( filename = "")``

with

  *filename*:
	The filename. If empty, overwrite the file
"""
		if  filename != "":
			self.filename = filename
			
		zip = zipfile.ZipFile(self.filename, 'w') 
	    for name in os.listdir(self.tmpdir):
			#print name
			zip.write(self.tmpdirname + name, name)
		
		zip.close()
		
		
    ######################################################################
    # add_comment( text )
    #
    # 2008-02-12 
    #		
   	def add_comment(self, text ):
		"""Add a simple comment to the gamera.txt file in the Aruspix file.

Signature:

  ``add_comment( text )``

with

  *text*:
	The comment that is going to be appended to gamera.txt
"""	
		f = open( self.tmpdirname + "gamera.txt", "a" )
		f.write( text ) 
		f.close()
	
	
	
    ######################################################################
    # get_img0()
    #
    # 2008-01-15 
    #		
   	def get_img0(self):
		"""Returns the image img0 (pre-classified image) from the Aruspix file.
		
Signature:

  ``get_img0()``
"""
		if os.path.exists(self.tmpdirname + "img0.tif") == False:
			return None
		else:
			return load_image(self.tmpdirname + "img0.tif")
			
		
    ######################################################################
    # get_img1()
    #
    # 2008-01-15 
    #		
   	def get_img1(self):
		"""Returns the image img1 (original greyscale image) from the Aruspix file.

Signature:

  ``get_img1()``
"""
  		if os.path.exists(self.tmpdirname + "img1.tif") == False:
			return None
		else:
			return load_image(self.tmpdirname + "img1.tif")

    ######################################################################
    # TifFile
    #
    # 2010-05-14 Gabriel Vigliensoni 
    #

class TifFile:
	def __init__(self, filename, tmpdir):
		self.f = filename
		self.t = tmpdir
	def filename(self):
		return self.f
		
    ######################################################################
    # dirEntries
    #
    # 2010-05-19 Gabriel Vigliensoni 
    #

class Tools:
	@staticmethod	
	def dirEntries(dir_name, subdir, *args):
		fileList = []
		for files in os.listdir(dir_name):
			dirfile = os.path.join(dir_name, files)
			if os.path.isfile(dirfile):
				if not args:
					fileList.append(dirfile)
				else:
					if os.path.splitext(dirfile)[1][1:] in args:
						fileList.append(dirfile)
			# recursively access file names in subdirectories
			elif os.path.isdir(dirfile) and subdir:
				#print "Accessing directory:", dirfile
				fileList.extend(Tools.dirEntries(dirfile, subdir, *args))
		return fileList
		


					
					
# GVM















