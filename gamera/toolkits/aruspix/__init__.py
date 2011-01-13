# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

"""
Toolkit setup

This file is run on importing anything within this directory.
Its purpose is only to help with the Gamera GUI shell,
and may be omitted if you are not concerned with that.
"""
import sys
import re
import os # GVM
import fnmatch # GVM
import plugins
import subprocess # GVM

from gamera import knn
from gamera.core import *
from gamera.args import *
from gamera.gui import gui
from gamera.gui import has_gui
from gamera.toolkits.aruspix.ax_file import AxFile
from gamera.toolkits.aruspix.ax_file import TifFile # GVM
from gamera.toolkits.aruspix.ax_file import Tools # GVM
#from gamera.toolkits.aruspix.ax_page import AxPage # GVM
#from gamera.toolkits.aruspix.ax_staff import AxStaff # GVM
from gamera.toolkits.aruspix.plugins import *
from gamera import toolkit

#from aruspi import PsaltikiPage

if has_gui.has_gui:
    from gamera.gui import var_name
    import wx # GVM from wxPython.wx import * 
    import aruspix_module_icon

    class AruspixPageModuleIcon(toolkit.CustomIcon):

        def __init__(self, *args, **kwargs):
            toolkit.CustomIcon.__init__(self, *args, **kwargs)

        def get_icon():
            return toolkit.CustomIcon.to_icon(\
                    aruspix_module_icon.getBitmap())
        get_icon = staticmethod(get_icon)

        def check(data):
            import inspect
            return inspect.ismodule(data) and\
                    data.__name__.endswith("aruspix")
        check = staticmethod(check)

        def right_click(self, parent, event, shell):
            self._shell = shell
            x, y = event.GetPoint()
            menu = wx.Menu() # GVM menu=wxMenu()

            # create the menu entry for each class listed in
            # 'classes' (they all point to the same method but
            # can be distinguished by their menu index)
            index = 1
            menu.Append(index, "Open Aruspix file")
            wx.EVT_MENU(parent, index, self.openAxFile) #GVM wxEVT_MENU(parent, index, self.openAxFile)
            # GVM
            index = 2 # index += 1 # GVM
            menu.Append(index, "Send files to Aruspix") # GVM
            wx.EVT_MENU(parent, index, self.openTifFile) # GVM
            parent.PopupMenu(menu, wx.Point(x, y)) #GVM parent.PopupMenu(menu, wxPoint(x, y))

        def double_click(self):
            pass
        #
        # creates an instance of a PsaltikiPage class
        #
        def openAxFile(self, event):
            #
            # let the user choose the parameters
            #
            #pp_module="PsaltikiPage"

            axfilename = ""
            tmpdir = ""
            imgdir = ""
            imgvisual = True
            imgmusic = True
            imglyrics = False
            imgborder = False
            imgornate = False
            imgtext = False
            imgtitle = False
            imgflat = False
            imggrey = False
            #opt = c_opt()
            # start options dialog
            dialog = Args([FileOpen("Aruspix file", axfilename, "*.axz"),
                #Directory("or all Aruspix Files in folder", imgdir),
                Directory("Temporary directory (optional)", tmpdir),
                Check("Visualize image","",True),
                Check("Extract music staves","",True),
                Check("Extract lyrics"),
                Check("Extract title elements"),
                Check("Extract ornate letters"),
                Check("Extract text in staff"),
                Check("Extract borders"),
                Check("Flatten as BW"),
                Check("Original greyscale image")],
                name = "Select options")
            
            params = dialog.show()

            if not params:
                return

            i = 0
            axfilename = params[i]; i+=1
            if axfilename == "":
                return
            tmpdir = params[i]; i+=1
            if tmpdir == None:
                tmpdir = ""
            imgvisual = params[i]; i+=1
            imgmusic = params[i]; i+=1
            imglyrics = params[i]; i+=1
            imgborders = params[i]; i+=1
            imgornate = params[i]; i+=1
            imgtext = params[i]; i+=1
            imgtitle = params[i]; i+=1
            imgflat = params[i]; i+=1
            imggrey = params[i]; i+=1
            
            axfile = AxFile(axfilename, tmpdir)
        
            global swap
            swap = axfile.get_img0()
    
            if imgvisual == True:
                name = var_name.get("aruspix_img",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.visualize()"\
                    % (name, self.label ))
        
            if imgmusic == True:
                name = var_name.get("staves",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.extract(0)"\
                    % (name, self.label ))
        
            if imglyrics == True:
                name = var_name.get("lyrics",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.extract(4)"\
                    % (name, self.label ))

            if imgborders == True:
                name = var_name.get("borders",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.extract(1)"\
                    % (name, self.label ))

            if imgornate == True:
                name=var_name.get("ornate_letters",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.extract(2)"\
                    % (name, self.label ))

            if imgtext == True:
                name=var_name.get("text_in_staff",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.extract(3)"\
                    % (name, self.label ))

            if imgtitle == True:
                name=var_name.get("titles",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.extract(5)"\
                    % (name, self.label ))

            if imgflat == True:
                name=var_name.get("all",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.flatten()"\
                    % (name, self.label ))

            if imggrey == True:
                swap = axfile.get_img1()
                name=var_name.get("original",\
                    self._shell.locals)
                self._shell.run("%s = %s.swap.image_copy()"\
                    % (name, self.label ))      
    
    ######################################################################
    # TifFile
    #
    # 2010-05-14 Gabriel Vigliensoni 
    #

        def openTifFile(self, event):
            
            tiffilename = ""
            foldir = ""
            global swap2
            alist = []


            dialog = Args([FileOpen("Send a .tif or .png file to Aruspix", tiffilename, "*.tif;*.png"), #
                #FileOpen("or a .png file", tiffilename, "*.tif;*.png"),
                Directory("or all .tif and .png files in folder", foldir)],
                name = "Open")
                
            params = dialog.show()  
            #print; print "params"; print params; print 
    
            if not params:
                return      
            if params[0]:   
            #   print 'it is a single file: '
            #   print params[0]
                alist.append(params[0])
            else:                           ## It is a folder
            #   print "yes! a folder"; print
                alist = Tools.dirEntries(params[1], True, 'tif', 'png')

            #app_path = '/Users/gabriel/Documents/code/aruspix/Debug/Aruspix.app/Contents/MacOS/Aruspix'    
            app_path = '/Applications/Aruspix.app/Contents/MacOS/Aruspix'
            #print; print 'alist: '; print alist; print 
            
            for i_file in alist:
                print 'Processing '; print i_file; print
                o_file = os.path.splitext(i_file); #print 'o_file'; print o_file; print
                if o_file[1] == '.png':
            #       print; print "PNG"
                    f = 'convert ' + i_file + ' -compress None ' + o_file[0] + '.tif' 
                    subprocess.Popen(f, shell = True)
                    f = app_path + ' -q -e Rec -p ' + o_file[0] + '.tif ' + o_file[0] + '.axz'
                    p = subprocess.Popen(f, shell = True)
                    p.wait()
                    subprocess.Popen("rm " +  o_file[0] + '.tif' , shell=True)  # erasing the created TIF               
                else:
            #       print; print "TIF"
                    f = app_path + ' -q -e Rec -p ' + i_file + ' ' + o_file[0] + '.axz'
                    p = subprocess.Popen(f, shell = True)
                    p.wait()                
        
                if params[0]:
                    axfilename = o_file[0] + '.axz' #; print "axfilename: "; print axfilename; print
                    axfile = AxFile(axfilename, "")
                    swap2 = axfile.get_img0()       #; print"swap: "; print swap2; print
                    name = var_name.get("aruspix_img",\
                        self._shell.locals)
                    self._shell.run("%s = %s.swap2.visualize()"\
                        % (name, self.label ))
                print 'Done!'
                print

# GVM

    AruspixPageModuleIcon.register()
