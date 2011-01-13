#ifndef aruspix_fill_white
#define aruspix_fill_white

#include "gamera.hpp"
#include "pixel.hpp"
#include <string.h>
#include <stdlib.h>
#include <plugins/morphology.hpp>
#include <plugins/arithmetic.hpp>

namespace Gamera {

/*
 * extract on plan (pixel value) in the image
 * 1 = music elements
 * 2 = borders
 * 3 = ornate letters
 * 4 = text in staff
 * 5 = lyrics
 * 6 = title
 */
template<class T>
OneBitRleImageView* extract(const T &src, int ex_type)
{
  typedef typename T::value_type value_type;
  int x,y;

  OneBitRleImageData* dest_data = new OneBitRleImageData(src.size(), src.origin());
  OneBitRleImageView* dest = new OneBitRleImageView(*dest_data);
  OneBitPixel blackval = black(*dest);
  OneBitPixel whiteval = white(*dest);
	
  ex_type = VIGRA_CSTD::pow(2.0,(ex_type));

  for (y = 0; y < (int)src.nrows(); y++)
    for (x = 0; x < (int)src.ncols(); x++) {
      if (src.get(Point(x,y))==ex_type)
			dest->set(Point(x,y),blackval);
	  else
			dest->set(Point(x,y),whiteval);
    }
  return dest;
}

template<class T>
RGBImageView* visualize(const T &src )
{
  typedef typename T::value_type value_type;	
  int x,y;

  RGBImageData* dest_data = new RGBImageData(src.size(), src.origin());
  RGBImageView* dest = new RGBImageView(*dest_data);
  RGBPixel blackval = black(*dest);
  RGBPixel whiteval = white(*dest);

  for (y = 0; y < (int)src.nrows(); y++)
    for (x = 0; x < (int)src.ncols(); x++) {
	  switch (src.get(Point(x,y))) {
		case (1) : dest->set(Point(x,y),blackval); break; // black, music
		case (2) : dest->set(Point(x,y),RGBPixel(228, 228, 228)); break; // light grey, border
		case (4) : dest->set(Point(x,y),RGBPixel(0, 127, 0)); break; // dark green, ornate letter
		case (8) : dest->set(Point(x,y),RGBPixel(0, 255, 0)); break; // light green, text in staff
		case (16) : dest->set(Point(x,y),RGBPixel(255, 127, 0)); break; // orange, lyrics
		case (32) : dest->set(Point(x,y),RGBPixel(255, 227, 0)); break; // yellow, title
		case (64) : dest->set(Point(x,y),RGBPixel(0, 0, 255)); break; // blue, UNUSED
		case (128) : dest->set(Point(x,y),RGBPixel(255, 0, 255)); break; // magenta, UNUSED
		default : dest->set(Point(x,y),whiteval);
	  }
    }
  return dest;
}

template<class T>
OneBitImageView* flatten(const T &src )
{
  typedef typename T::value_type value_type;
  int x,y;

  OneBitImageData* dest_data = new OneBitImageData(src.size(), src.origin());
  OneBitImageView* dest = new OneBitImageView(*dest_data);
  OneBitPixel blackval = black(*dest);
  OneBitPixel whiteval = white(*dest);

  for (y = 0; y < (int)src.nrows(); y++)
    for (x = 0; x < (int)src.ncols(); x++) {
      if (src.get(Point(x,y))!=0)
			dest->set(Point(x,y),blackval);
	  else
			dest->set(Point(x,y),whiteval);
    }
  return dest;
}

}

#endif
