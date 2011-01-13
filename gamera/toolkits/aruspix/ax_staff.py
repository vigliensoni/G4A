# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

#import image_utilities

import os


##############################################################################
class AxStaff:
##############################################################################
    """Class for storing a list of image objects.

An object of the class *AxStaff* provides the following functionality:

 - Storing all connected components (glyphs) of a staff in a list
 - Providing information about the staff position
 - Sorting glyphs by their x positions in the staff
 - Output of all glyphs in a specified format

The constructor_ of a *AxStaff* object adds several public properties
to each image of its image list.

.. _constructor: gamera.toolkits.aruspix.ax_staff.AxStaff.html#init

:Author: Laurent Pugin and Jason Hockman
"""

    ######################################################################
    # constructor
    #
    def __init__(self, staff, staff_height, ymax, staffspace_height, staffline_height):
        """Creates and returns a *AxStaff* object.

Signature:

  ``__init__(staff, staff_height, ymax, staffspace_height, staffline_height)``

with

  *staff*:
    StaffObj as return by get_staffpos from ``MusicStaves``

  *staff_height*:
    The staff bounding box height, as specified in AxPage

  *ymax*:
    The maximum y value, i.e. as in the original image (to avoid 
    overflow).

A *AxStaff* contains the public properties as described below:

+-----------------------+---------------------------------------------------+
| TODO                  |                                                   |
+-----------------------+---------------------------------------------------+

Additionally, new public properties are introduced in the constructor of this
object

+-----------------------+---------------------------------------------------+
| TODO                  |                                                   |
+-----------------------+---------------------------------------------------+

"""
        self.glyphs=[] # list of glyphs
                # the glyphs are added in set_glyph
        self.ground_truth_glyphs=[] # the list of ground truth glyphs
                # their are loaded in load_ground_truth
        self.staffno=staff.staffno
        self.yposlist=staff.yposlist
        # the y centroid of the staff is given by the average of the yposlist
        self.center_y=0
        if len(self.yposlist):
            self.center_y = sum(self.yposlist)/len(self.yposlist)
        # now we can compute the upper and lower y bounding box
        self.bbox_ymin = max(0, self.center_y - staff_height / 2)
        self.bbox_ymax = min(ymax, self.center_y + staff_height / 2)
        self.staffspace_height = staffspace_height
        self.staffline_height = staffline_height
        # for debugging
        # print "Staff", self.staffno, ": center_y", self.center_y, "bbox_ymin", self.bbox_ymin, "bbox_ymax", self.bbox_ymax
        # print staffspace_height
        
        
        
    #####################################################################
    # int __get_ground_truth_glyph(glyph_x)
    #
    # parameters:
    #      glyph_x: the x value of the glyph that is going to be used to
    #       find the ground_truth_glyph to which it belongs
    #
    # returns the ground_truth_glyph index, -1 if out of range
    #
    # 2008-02-08
    #   
    def __get_ground_truth_glyph(self, glyph_x):
        # nothing if no staff on the page
        if len(self.ground_truth_glyphs)==0:
            return -1

        i=0
        for gtg in self.ground_truth_glyphs:    
            #print glyph_x, gtg[0], gtg[1], gtg[2], len(gtg[3])
            if (glyph_x > int(gtg[0]) and glyph_x < int(gtg[1])): # that's the one
                return i
            elif (glyph_x < int(gtg[0])): # just to stop here..
                return -1
            i+=1

        return -1   

    ######################################################################
    # load_ground_truth( dirname, minsize, no_group )
    #
    # 2008-01-15
    #
    def load_ground_truth( self, dirname="", minsize=5, no_group=False ):
        """Load the ground truth file staff_X_0.nplab, where X is the staffno - 1.
This method ignore the staff segments and load only the first one (usually there is 
only one, so it will load most of the ground truth data)

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
        self.ground_truth_glyphs=[]
        # generate file name and check if it exists
        fname = dirname + "staff_" + str(self.staffno -1) + ".0.nplab"
        #print fname
        if os.path.exists(fname) == False:
            print "file", fname, "not found"
            return

        # laod the file
        f = open( fname, "r" )
        for line in f.read().split('\n'):
            if line == "":
                continue
            tokens = line.lower().split()
            # skip line if there is no 3 elements (x1 x2 name)
            if len(tokens) < 3:
                continue
            self.ground_truth_glyphs.append([tokens[0],tokens[1],tokens[2],[]])
            
        #for gl in self.ground_truth_glyphs:    
        #   print gl[0], gl[1], gl[2], len(gl[3])
        #print len(self.ground_truth_glyphs)
            
        # label the glyphs according to the positions
        for gl in self.glyphs:
            gl.middle_x=int(gl.offset_x+gl.ncols*0.5)
            # skip small glyphs
            if (gl.ncols < minsize or gl.nrows < minsize):
                continue
            # we use the middle x point of the glyph as reference
            g = self.__get_ground_truth_glyph(gl.middle_x)  
            if (g != -1):
                #print "add to ", self.ground_truth_glyphs[g][2]
                self.ground_truth_glyphs[g][3].append(gl)
            #else:
                #print "Skip glyph", gl.id_name, "at position", gl.middle_x
        
        # label the glyphs according to the positions
        for gtg in self.ground_truth_glyphs:
            for gl in gtg[3]:
                name = gtg[2]
                if len(gtg[3]) > 1:
                    if (no_group==True):
                        continue
                    name = "_group._part." + name
                    t = [(1.0/len(gtg[3]), name)] # confidence and name
                    # group, classify heuristic
                    gl.classify_heuristic(t)
                else:
                    t = [(1.0/len(gtg[3]), name)] # confidence and name
                    # manually classifiy
                    gl.classify_manual(t) 

    ######################################################################
    # add_glyph( glyphs )
    #
    # 2008-01-15
    #
    def add_glyph( self, glyph ):
        """Add the glyph to the staff. Sort according to the middle_x position

Signature:

  ``add_glyph( glyph )``

with

  *glyph*:
    The glyph that is going to be added.
"""     
        self.glyphs.append(glyph)
        self.glyphs.sort(lambda x, y: cmp(x.middle_x,y.middle_x))

    ######################################################################
    # output( )
    #
    # output the content of the staff
    #
    ######################################################################
    def __pitch_point(self,rel_pitch_pixel,pitch_height):
        """returns the pitch value for a given pitch point"""
        notes = ['C','D','E','F','G','A','B']
        note = 0        
        idx = (rel_pitch_pixel) / (pitch_height)
        if idx >= 0:
            if abs(rel_pitch_pixel - (idx+1)*pitch_height) < abs(rel_pitch_pixel - (idx)*pitch_height):
                idx = idx + 1
            note = idx % 7
        else:
            if abs(rel_pitch_pixel - (idx-1)*pitch_height) < abs(rel_pitch_pixel - (idx)*pitch_height):
                idx = idx - 1
            note = (7 + idx) % 7
        octave = int(idx / 7)+4
        notecode = notes[note] + "_" + str(octave) 
        return [idx, notecode]
    ######################################################################
    def __clef_point(self,rel_pitch_pixel,clef_step):
        """returns the clef for a given pitch point"""      
        idx = (rel_pitch_pixel) / (clef_step)
        if idx < 0:
            idx = 0
        if abs(rel_pitch_pixel - (idx+1)*clef_step) < abs(rel_pitch_pixel - (idx)*clef_step):
            idx = idx + 1
        if idx > 4:
            idx = 4
        return idx + 1
        
    ######################################################################
    def __column_pixel_count(self,gly,ref_flag):
        """returns pitch of note based on black pixels remaining"""
        gly_proj = gly.projection_rows()
        if ref_flag == 1:
            ref_pos = gly.ul_y
            pitch = (len(gly_proj)/2)+ref_pos
        else:
            ref_pos = gly.ll_y
            pitch = ref_pos - (len(gly_proj)/2)
        return pitch
    ######################################################################
    def __rest_type_flag(self,center_pos,pitch_height):
        """returns new str_id for misclassified R_2/R_3 glyphs"""
        rest_flag = abs((center_pos-self.yposlist[-1])/(pitch_height)) % 2
        if center_pos < self.yposlist[-1]:
            if rest_flag == 0:
                str_id = "R_2"
            else:
                str_id = "R_3"
        else:
            if rest_flag == 1:
                str_id = "R_2"
            else:
                str_id = "R_3"
        return str_id
    ######################################################################
    def __max_index(self, any_array):
        """returns max index"""
        max_val = max(any_array)
        n = []
        for k,v in enumerate(any_array):
            if v == max_val:
                n += [k]
        return sum(n)/len(n)
    ######################################################################
    def __min_index(self, any_array):
        """returns min index"""
        min_val = min(any_array)
        n = []
        for k,v in enumerate(any_array):
            if v == min_val:
                n += [k]
        return sum(n)/len(n)
        return n
    ######################################################################
    
    
    def output( self ):
        """Output the content of the staff, glyph by glyph.
        
Signature:

    ``output( )``
"""
        
        res = ""
        # for each glyph in staff
        for gl in self.glyphs:
            # str_id is the glyph name
            str_id = str(gl.id_name)
            # find string character number bt. 2 items in id_name
            b = str_id.find(' ') + 2
            # condense str_id by removing last characters
            str_id = str_id[b:-3]   
            # replace the . with a _
            str_id = str_id.replace ('.','_')
            # capitalize string
            str_id = str_id.upper()
            # if str_id starts with a N
            if str_id.startswith('N'):
                # replace _ with .
                str_id = str_id.replace('_','.')
                # replace . with _ followed by 1 for flags
                str_id = str_id.replace ('.','_',1)
            
            # ****************************
            if str_id == "SKIP":
                continue
            else:
            
            
                # # pitch from c1
                # pitch_from_c1 = -(gl.center_y - self.yposlist[len(self.yposlist)-1]) / \
                #             (len(self.yposlist)-1) / 2
                # # note value (0 - 7) relating to "notes" above

                # center y position of the glyph - used in a few 
                center_pos = gl.center_y
                upper_pos = gl.ul_y
                lower_pos = gl.ll_y
                pitch_height = (self.staffspace_height+self.staffline_height)/2
                ### PITCH POINTS ###
                pp_flag = 0
                gflag = 0
                aflag = 0
                # A_B0 - projection, then find max
                if str_id.startswith('A_B0'):
                    dummy_1 = gl.contour_left()
                    dummy_2 = gl.contour_right()
                    row_width = []
                    for n in range(0,len(dummy_1)):
                        row_width += [dummy_1[n]+dummy_2[n]]
                    pitch = self.__min_index(row_width) + upper_pos
                    pp_flag = 1

                # A_B1 - projection, then find max of lower half
                elif str_id.startswith('A_B1'):
                    gly = gl.splity()[1]
                    dummy_1 = gly.contour_left()
                    dummy_2 = gly.contour_right()
                    row_width = []
                    for n in range(0,len(dummy_1)):
                        row_width += [dummy_1[n]+dummy_2[n]]
                    pitch = self.__min_index(row_width) + center_pos
                    pp_flag = 1

                # A_D0, A_H0
                elif str_id.startswith('A_D0') | str_id.startswith('A_H0'):
                    pitch = center_pos
                    pp_flag = 1
                # A_D1 - cut off top, get reference position and width of new box
                elif str_id.startswith('A_D1'):
                    gl = gl.splity()[1]
                    ref_pos = gl.ll_y
                    pitch = gl.ll_y - (gl.width/2)
                    pp_flag = 1
            
                # custos
                elif str_id.startswith('C'):
                    gly = gl.splitx_left()[0]
                    pitch = gly.center_y
                    pp_flag = 1
                # dot
                elif str_id.startswith('P'):
                    pitch = center_pos
                    pp_flag = 1
                            
                # K
                elif str_id.startswith('K_U') | str_id.startswith('K_C'):
                    pitch = center_pos
                    pp_flag = 2 
                
                elif str_id.startswith('K_S'):
                    pitch = center_pos
                    str_id = "K_S2"
            
                ## NOTES ##
            
                # N_O
                elif str_id.startswith('N_0'):
                    gl = gl.splitx_left()[0]
                    if str_id.endswith('.1'):
                        pitch = self.__column_pixel_count(gl,0)
                    else:
                        pitch = self.__column_pixel_count(gl,1)
                    if str_id.endswith('.1'):
                        gflag = 1
                    else:
                        gflag = 0
                    pp_flag = 1
                
                # N_1, N_2
                elif str_id.startswith('N_1') | str_id.startswith('N_2'):
                    pitch = center_pos
                    pp_flag = 1
            
                # N_3
                elif str_id.startswith('N_3'):
                    dummy_1 = gl.contour_left()
                    dummy_2 = gl.contour_right()
                    row_width = []
                    for n in range(0,len(dummy_1)):
                        row_width += [dummy_1[n]+dummy_2[n]]
                        pitch = self.__min_index(row_width) + upper_pos
                    if str_id.endswith('.1'):
                        gflag = 1
                    else:
                        gflag = 0
                    pp_flag = 1
            
                # N_4, N_5, N_6        
                elif str_id.startswith('N_4') | str_id.startswith('N_5') | str_id.startswith('N_6'):
                    gly_proj = gl.projection_rows()
                    if str_id.endswith('.1'):
                        gly_proj = gly_proj[len(gly_proj)/2:len(gly_proj)]
                        pitch = self.__max_index(gly_proj) + center_pos
                        gflag = 1
                    else:
                        gly_proj = gly_proj[0:len(gly_proj)/2]
                        pitch = self.__max_index(gly_proj) + upper_pos
                        gflag = 0
                    pp_flag = 1
            
                # RESTS
                elif str_id.startswith('R'):
                    # R_2, R3
                    if str_id.startswith('R_2') | str_id.startswith('R_3'):
                        str_id = self.__rest_type_flag(center_pos,pitch_height)
                        if str_id == ('R_2'):
                            pitch = upper_pos
                        else:
                            pitch = lower_pos
                    # R_0, R_1, R_4    
                    elif str_id.startswith('R_0') | str_id.startswith('R_1') | str_id.startswith('R_4'):
                        # lower position
                        pitch = lower_pos
                    pp_flag = 1
                
                # create final name for glyph
                if pp_flag == 1:
                    index, notecode = self.__pitch_point(self.yposlist[-1] - pitch, pitch_height)
                    if str_id.endswith('.1'):
                        str_id = str_id.strip('.1')
                    elif str_id.endswith('.4'):
                        str_id = str_id.strip('.4')
                        aflag = 4
                    if str_id.startswith('N') and not str_id.startswith('N_2') and not str_id.startswith('N_1'):
                        if (index <= 4):
                            if gflag == 1:
                                aflag = 0
                            else:
                                aflag = 1
                        else:
                            if gflag == 1:
                                aflag = 1
                            else:
                                aflag = 0
                
                    if aflag > 0:
                        str_id = str_id + "_" + notecode + "_" + str(aflag)
                    else:
                        str_id = str_id + "_" + notecode
                elif pp_flag == 2:
                    index = self.__clef_point(self.yposlist[-1] - pitch, self.staffspace_height + self.staffline_height)
                    str_id = str_id + str(index)
                # print str_id
                    
                # res is the staff number that houses the glyphs
                res += str(gl.offset_x) + " " + str(gl.offset_x+gl.ncols) + " " + str_id + "\n"
        
        if len(res) == 0:
            return res # do not print empty staves
            
        # standard header for the staff
        outstr = "\"*/staff_" + str(self.staffno - 1) + ".0.lab\"\n"
        outstr += res
        outstr += ".\n"
        return  outstr


    def output_nopitch( self ):
        """Output the content of the staff, glyph by glyph.

Signature:

    ``output_nopitch( )``
"""     
        res = ""
        # for each glyph in staff
        for gl in self.glyphs:
            # str_id is the glyph name
            str_id = str(gl.id_name)
            # find string character number bt. 2 items in id_name
            b = str_id.find(' ') + 2
            # condense str_id by removing last characters
            str_id = str_id[b:-3]   
            # replace the . with a _
            str_id = str_id.replace ('.','_')
            # capitalize string
            str_id = str_id.upper()
            # if str_id starts with a N
            if str_id.startswith('N'):
                # replace _ with .
                str_id = str_id.replace('_','.')
                # replace . with _ followed by 1 for flags
                str_id = str_id.replace ('.','_',1)
                
            # ****************************
            if str_id == "SKIP":
                continue
            else:   
                res += str(gl.offset_x) + " " + str(gl.offset_x+gl.ncols) + " " + str_id + "\n"

        if len(res) == 0:
            return res # do not print empty staves

        # standard header for the staff
        outstr = "\"*/staff_" + str(self.staffno - 1) + ".0.lab\"\n"
        outstr += res
        outstr += ".\n"
        return  outstr
