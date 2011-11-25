# Muuse - Yet another audio player
#
# Copyright (c) 2011 Joel Griffith
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import sys
import os

import pygtk
pygtk.require('2.0')
import gtk

IMAGES_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'images')

def get_image(uri):
	img = gtk.Image()
	img.set_from_file(uri)
	return img
	
def get_icon_uri(name):
    return os.path.join(IMAGES_PATH, '%s.png' % name)
    
def get_icon(name):
    return get_image(get_icon_uri(name))
        
