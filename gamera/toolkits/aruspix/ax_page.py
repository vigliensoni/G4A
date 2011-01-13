# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

##############################################################################
# ax_page.py
#
# 2008-01-15
#
##############################################################################

from gamera.core import *
#from gamera.toolkits.musicstaves import MusicStaves_rl_fujinaga as MusicStaves
from gamera.toolkits.musicstaves import MusicStaves_linetracking as MusicStaves
# LP but I assume that we would need all of them
#from gamera.toolkits.musicstaves import *
from gamera.toolkits.aruspix.ax_staff import AxStaff

# LP rough adaptation from otr_staff.py, leave you check what is needed...
class AxPage:
##############################################################################
    """Stores a tablature and its information (e.g. staff position).
    
An object of this class provides the following functionality:

- Staff line removal
- Return the information *staff number* for a given (x,y) position
- Return a list of staff bounding boxes
- Removal of regions outside any staff

.. note:: The removal of the staff lines is done by the inherited
          *MusicStaves* object. Thus, the *MusicStaves* toolkit is required.

A *AxPage* object has several public properties, that can be manipulated by
the user. The following table gives a detailed view on this.

+-----------------------+---------------------------------------------------+
| ``music_staves``      | The inherited *MusicStaves* object.               |
+-----------------------+---------------------------------------------------+
| ``image``             | A reference to ``music_staves.image``             |
|                       | (for convenience).                                |
+-----------------------+---------------------------------------------------+
| ``staffline_height``  | A reference to ``music_staves.staffline_height``  |
+-----------------------+---------------------------------------------------+
| ``staffspace_height`` | A reference to ``music_staves.staffspace_height`` |
+-----------------------+---------------------------------------------------+
| ``staff_height``      | The staff bounding box height                     |
+-----------------------+---------------------------------------------------+

.. _constructor: gamera.toolkits.aruspix.ax_page.AxPage.html#init

:Author: Laurent Pugin and Jason Hockman
"""

    ######################################################################
    # constructor
    #
    # 2008-01-15
    #
    def __init__(self, img, staffline_height=0, staffspace_height=0):
        """Constructs and returns a *AxPage* object.
        
Signature:

  ``__init__(img, staffline_height=0, staffspace_height=0)``

with

  *img*:
    Onebit or greyscale image a *AxPage* should be created of.

  *staffline_height*:
    Vertical thickness of a staff line. When not specified here, it will be
    detected automatically.

  *staffspace_height*:
    Thickness of the vertical space between adjacent staff lines. When not
    specified here, it will be detected automatically.
"""

        self.image=None      # image of the tablature (reference to
                     # self.music_staves.image, see below)
        self.stafflist=[]    # list of AxStaff objects
                     # the list is created in remove_staves

        self.num_lines=0 # number of lines in the staves
                     # value is given of computed in remove_staves
        self.staff_height=0 # staff bounding box height
                    # value is given or computed in remove_staves

        # use external class module for removing the staves
        self.music_staves=MusicStaves(img, staffline_height,\
                staffspace_height)

        # references to important information
        self.image=self.music_staves.image
        self.staffline_height=self.music_staves.staffline_height
        self.staffspace_height=self.music_staves.staffspace_height


    #####################################################################
    # int __get_staffno(glyph_y)
    #
    # parameters:
    #      glyph_y: the y value of the glyph that is going to be used to
    #       find the staff to which it belongs
    #
    # returns the staff index, -1 if out of range
    #
    # 2008-01-15
    #   
    def __get_staffno(self, glyph_y):
        # nothing if no staff on the page
        if len(self.stafflist)==0:
            return -1

        for st in self.stafflist:
            if (glyph_y > st.bbox_ymin and glyph_y < st.bbox_ymax): # that's the one
                return st.staffno - 1
            elif (glyph_y < st.bbox_ymax): # just to stop here..
                return -1
                
        return -1

    ######################################################################
    # remove_staves( crossing_symbols, num_lines, staff_height)
    #
    # 2008-01-15 
    #
    def remove_staves(self, crossing_symbols='bars', num_lines=0, staff_height=0):
        """Detects and removes staff lines from a music image.

Signature:

  ``remove_staves(crossing_symbols='bars', num_lines=0, staff_height=0)``

with

  *crossing_symbols*:
    Determines which symbols crossing staff lines the removal should try
    to keep intact. In addition to the possible values are ``all``, ``bars``
    and ``none`` (see the MusicStaves module for details).
  
  *num_lines*:
    Number of lines within one staff. A value of zero means, that this number
    should be guessed automatically.

  *staff_height*:
    Staff bounding box height. If not specified, it is automatically computed
    with one staffspace_height above and below.
"""

        self.num_lines=num_lines # number of lines in the staves
        self.staff_height=staff_height # staff bounding box height

        self.music_staves.remove_staves(\
                crossing_symbols=crossing_symbols,\
                num_lines=num_lines)

        slist = self.music_staves.get_staffpos()

        # we assume that all staves have the same number of lines
        if (len(slist) > 0 and self.num_lines==0):
            self.num_lines = len(slist[0].yposlist)
        
        # just add one staffspace_height above and below    
        if (self.num_lines != 0 and self.staff_height==0):
                self.staff_height = self.num_lines * self.staffline_height\
                 + (self.num_lines + 1) * self.staffspace_height
                
        print "Number of staves:", len(slist)

        # create the stafflist
        self.stafflist = []
        for s in slist:
            st = AxStaff(s, self.staff_height, self.image.nrows, self.staffspace_height, self.staffline_height)
            self.stafflist.append(st)
            
        ##for i,s in enumerate(self.stafflist):
        ##    print "    Staff", s.staffno, ":", s.yposlist,\
        ##          "   Range:", self.staffranges[i]

        # make self.image a reference to the actual
        # image of the MusicStaves object
        self.image=self.music_staves.image


    ######################################################################
    # add_glyphs( glyphs )
    #
    # 2008-01-15
    #
    def add_glyphs( self, glyphs ):
        """Add the glyphs to the page. Find the staff to which they belong.

Signature:

  ``add_glyphs( glyphs )``

with

  *glyphs*:
    The list of glyphs that are going to be added to the page. They must have 
    been classified before. The method will find the staff to which they belong.
"""     

        for gl in glyphs:
            gl.middle_x=int(gl.offset_x+gl.ncols*0.5)
            gl.middle_y=int(gl.offset_y+gl.nrows*0.5)
            
            # we use the middle y point of the glyph as reference
            s = self.__get_staffno(gl.middle_y) 
            if (s != -1):
                self.stafflist[s].add_glyph(gl)
            else:
                print "Skip glyph", gl.id_name, "at position", gl.middle_y
                
                
    ######################################################################
    # load_ground_truth( dirname, minsize, no_group )
    #
    # 2008-01-15
    #
    def load_ground_truth( self, dirname="", minsize=5, no_group=False ):
        """Load the ground truth for every staff.

Signature:

  ``load_ground_truth( dirname, minsize, no_group )``

with

  *dirname*:
    The directory where is the file.

  *minsize*:
    The size of the small glyph that will be considered. Skipped if smaller.

  *no_group*:
    Skip labels where more than one glyph per label. Otherwise add "_group._part"
as prefix
"""
        # the staff content...
        for st in self.stafflist:
            st.load_ground_truth( dirname, minsize, no_group )
            
                
    ######################################################################
    # output( )
    #
    # 2008-01-15
    #
    def output( self ):
        """Output the content of the page, staff by staff.
        
Signature:

    ``output( )``
"""     
        # standard header for Aruspix transcription files
        res = "#!MLF!#\n"

        # the staff content...
        for st in self.stafflist:
            res += st.output()
        res += "\n"
        return  res
