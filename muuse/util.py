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

import os
import pygtk
pygtk.require('2.0')
import gtk

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'images')

def format_time(seconds):
    time = ''
    # Don't show hours by default unless it's necessary
    if seconds >= 3600:
        time += '%(hours)02d:' % {'hours': seconds / 3600}
    while seconds >= 3600:
        seconds -= 3600
    # Always show minutes and seconds
    time += '%(minutes)02d:' % {'minutes': seconds / 60}
    while seconds >= 60:
        seconds -= 60
    time += '%(seconds)02d' % {'seconds': seconds}
    return time

def get_icon(name):
    return get_image(to_icon_uri(name))

def get_image(uri):
    img = gtk.Image()
    img.set_from_file(uri)
    return img

def to_icon_uri(name):
    return os.path.join(IMAGES_PATH, 
                        '%(name)s.png' % {'name': name})
    
