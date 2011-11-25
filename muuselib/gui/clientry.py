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

import re
import gobject
import pygtk
pygtk.require('2.0')
import gtk

class CLIEntry(gtk.Entry):
    def __init__(self, err_func=None, end_func=None, **cmds):
        gtk.Entry.__init__(self)

        self.err_func = err_func
        self.end_func = end_func
        self.cmds = cmds
        
        self.history = []
        
        self.connect("activate", self._activated)
        
    def _activated(self, widget, data=None):
        text = self.get_text()
        match = None
        for cmd, func in self.cmds.iteritems():
            match = re.match(cmd, text)
            if match:
                break
        
        if match:
            func(**match.groupdict())
        elif self.err_func is not None:
            self.err_func()
                
        if self.end_func is not None:
            self.end_func()
            
        if text:
            self.history.append(text)
