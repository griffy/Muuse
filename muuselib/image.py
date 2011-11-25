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
        
