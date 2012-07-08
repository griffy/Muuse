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

import gobject
import pygtk
pygtk.require('2.0')
import gtk

class ListBox(gtk.ScrolledWindow):
    def __init__(self, width, height, title=None,
                 column_type=gobject.TYPE_STRING,
                 select_type=gtk.SELECTION_SINGLE):
        gtk.ScrolledWindow.__init__(self)
        
        self.tree_view = gtk.TreeView()
        self.set_select_type(select_type)

        self.list_store = gtk.ListStore(column_type)

        self.tree_view.set_model(self.list_store)
        
        # this displays one column (all we need)
        self.tree_view_column = gtk.TreeViewColumn()
        """ Of the three options:
            GROW_ONLY, AUTOSIZE, and FIXED
            
            It makes most sense that the expected behavior, especially
            when it resides in a ScrolledWindow, would be for the column
            to have a set width which can be scrolled past if necessary
        """
        self.tree_view_column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        self.set_title(title)
            
        self.tree_view.append_column(self.tree_view_column)

        self.cell_renderer = gtk.CellRendererText()

        # add the cell and allow it to expand
        self.tree_view_column.pack_start(self.cell_renderer, False)
        
        self.tree_view_column.add_attribute(self.cell_renderer, 'text', 0)

        self.add_with_viewport(self.tree_view)
        # make the scrollbars only appear when needed
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_size_request(width, height)
        
        self.tree_view.connect('move_cursor', self._move_cursor)
        
    def connect(self, event, func):
        if event == 'row_activated':
            self.tree_view.connect(event, func)
        
    def _move_cursor(self, treeview, step, count, data=None):
        cur_index = self.get_selected_row()
        if cur_index:
            self.select_and_scroll(cur_index+count)
        return True
        
    def __len__(self):
        return len(self.list_store)
        
    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return [self[i] for i in range(*indices)]
        else:
            if index < 0:
                # Negative index means start from the end
                return self.list_store[len(self)+index][0]
            if 0 <= index < len(self):
                return self.list_store[index][0]
            
    def __setitem__(self, index, item):
        if 0 <= index < len(self):
            self.list_store[index] = [item]

    def __delitem__(self, index):
        if 0 <= index < len(self):
            del self.list_store[index]
        
    def __iter__(self):
        for item in self.get_all():
            yield item
            
    def __contains__(self, item):
        for row in self.list_store:
            if row[0] == item:
                return True
        return False
        
    def append(self, item):
        self.list_store.append([item])

    def extend(self, items):
        for item in items:
            self.list_store.append([item])
            
    def insert(self, index, item):
        if index >= 0:
            self.list_store.insert(index, [item])
       
    def remove(self, item):
        del self[self.index(item)]
            
    def pop(self, index=None):
        if not index:
            index = len(self)-1
        if 0 <= index < len(self):
            item = self[index]
            del self[index]
            return item
            
    def index(self, item):
        for i, row in enumerate(self.list_store):
            if row[0] == item:
                return i
        raise Exception # make more specific later
        
    def count(self, item):
        count = 0
        for row in self.list_store:
            if row[0] == item: 
                count+=1
        return count
        
    # TODO: Implement sort() and reverse()
        
    def get_selected_row(self):
        rows = self.get_selected_rows()
        if rows: 
            return rows[0]
        return []
        
    def get_selected_rows(self):
        paths = self.tree_view.get_selection().get_selected_rows()[1]
        return [path[0] for path in paths]
        
    def get_selected_row_item(self):
        items = self.get_selected_row_items()
        if items:
            return items[0]
        return []
        
    def get_selected_row_items(self):
        paths = self.tree_view.get_selection().get_selected_rows()[1]
        return [self.list_store[path][0] for path in paths]
        
    def select_row(self, row):
        self.unselect_all()
        selection = self.tree_view.get_selection()
        selection.select_path(row)
        
    def select_rows(self, rows):
        self.unselect_all()
        selection = self.tree_view.get_selection()
        for row in rows:
            selection.select_path(row)
            
    def select_inverse(self):
        rows = self.get_selected_rows()
        if rows:
            new_rows = []
            for i in range(0, len(self)):
                if i in rows:
                    continue
                new_rows.append(i)
            self.select_rows(new_rows)
            
    def select_and_scroll(self, index, focus=False):
        self.select_row(index)
        
        vadj = self.get_vadjustment()
        
        page_size = vadj.page_size
        cell_height = self.tree_view_column.cell_get_size()[4]
        rows_per_page = int(page_size / cell_height)
        start_pos = int(vadj.value)
        end_pos = start_pos + (rows_per_page - 1) * cell_height
        selected_pos = index * cell_height
        
        bar = self.get_vscrollbar()
        if focus:
            bar.set_value(selected_pos - (rows_per_page / 2) * cell_height)
        elif selected_pos < start_pos:
            bar.set_value(selected_pos)
        elif selected_pos > end_pos:
            bar.set_value(selected_pos - page_size + cell_height)
            
    def remove_selected_rows(self):
        rows = self.get_selected_rows()
        rows.reverse()
        for row in rows:
            del self[row]
        
    def get_all(self):
        return [row[0] for row in self.list_store]
    
    def clear(self):
        self.list_store.clear()
        
    def select_all(self):
        self.tree_view.get_selection().select_all()
        
    def unselect_all(self):
        self.tree_view.get_selection().unselect_all()
		
    def set_fixed_row_height(self, fixed_height):
        self.tree_view.set_fixed_height_mode(fixed_height)
        
    def set_select_type(self, type):
        self.tree_view.get_selection().set_mode(type)
        
    def set_title(self, title):
        if title:
            # set the header to the text given
            self.tree_view_column.set_title(title)
            self.tree_view.set_headers_visible(True)
        else:
            self.tree_view_column.set_title('')
            self.tree_view.set_headers_visible(False)
