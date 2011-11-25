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
