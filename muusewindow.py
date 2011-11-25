import pygtk
pygtk.require('2.0')
import gtk
import pango

from muuselib.image import get_icon, get_icon_uri
from muuselib.gui.listbox import ListBox
from muuselib.gui.clientry import CLIEntry

WIDTH = 240
HEIGHT = 277

class MuuseWindow(object):
    def __init__(self):
        self.setup_tray_icon()
        self.setup_gui()
        self.setup_handlers()
		
    def setup_tray_icon(self):
        # create a status icon that sits in the tray
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(get_icon_uri('muuse'))
        self.status_icon.set_tooltip('Muuse')
        
        # create a menu for the status icon
        self.menu = gtk.Menu()
        self.menu_item_show = gtk.CheckMenuItem("Show Muuse")
        self.menu_item_show.set_active(True)
        self.menu_item_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menu.append(self.menu_item_show)
        self.menu.append(self.menu_item_quit)
        
    def setup_gui(self):
        # create the main window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Muuse')
        self.window.set_icon_from_file(get_icon_uri('muuse'))
        self.window.set_default_size(WIDTH, HEIGHT)
        
        # create the main content holder
        self.content_box = gtk.VBox(False, 0)
        
        # create content holder for top portion of the window
        self.top_box = gtk.VBox(False, 0)
        # create the label displaying info about currently playing audio file
        self.audio_label = gtk.Label('')
        self.audio_label.set_ellipsize(pango.ELLIPSIZE_END)
        # create the progress bar for the audio file that a user can click
        self.audio_slider = gtk.ProgressBar()
        # create a button box
        self.button_box = gtk.HBox(False, 0)
        # create the buttons
        self.play_btn = gtk.Button()
        self.play_btn.set_image(get_icon('play'))
        self.stop_btn = gtk.Button()
        self.stop_btn.set_image(get_icon('stop'))
        self.previous_btn = gtk.Button()
        self.previous_btn.set_image(get_icon('previous'))
        self.next_btn = gtk.Button()
        self.next_btn.set_image(get_icon('next'))
        self.repeat_btn = gtk.Button()
        self.repeat_btn.set_image(get_icon('repeatall'))
        self.shuffle_btn = gtk.Button()
        self.shuffle_btn.set_image(get_icon('shuffleoff'))
        self.volume_btn = gtk.VolumeButton()
        self.volume_btn.set_image(get_icon('volumemid'))
        self.volume_btn.set_value(0.5)
        # add them to the button box
        self.button_box.pack_start(self.play_btn, True, True, 0)
        self.button_box.pack_start(self.stop_btn, True, True, 0)
        self.button_box.pack_start(self.previous_btn, True, True, 0)
        self.button_box.pack_start(self.next_btn, True, True, 0)
        self.button_box.pack_start(self.repeat_btn, True, True, 0)
        self.button_box.pack_start(self.shuffle_btn, True, True, 0)
        self.button_box.pack_start(self.volume_btn, True, True, 0)
        # add everything so far to the top portion of the window
        self.top_box.pack_start(self.audio_label, False, True, 5)
        self.top_box.pack_start(self.audio_slider, False, True, 0)
        self.top_box.pack_start(self.button_box, False, True, 0)
        
        # create content holder for bottom portion of window
        self.bottom_box = gtk.VBox(False, 0)
        # create the listbox for audio to be added to
        self.listbox = ListBox(WIDTH, HEIGHT-77, 'Library')
        # create notebook to hold boxes below
        self.notebook = gtk.Notebook()
        # create box to hold cli
        self.cli_box = gtk.HBox(True, 0)
        self.cli = CLIEntry()
        self.cli_box.pack_start(self.cli, False, True, 0)
        # create box to hold add buttons
        self.add_box = gtk.HBox(True, 0)
        self.add_file_btn = gtk.Button("Add File")
        self.add_folder_btn = gtk.Button("Add Folder")
        self.add_box.pack_start(self.add_file_btn, False, True, 0)
        self.add_box.pack_start(self.add_folder_btn, False, True, 0)
        # create box to hold remove buttons
        self.rem_box = gtk.HBox(True, 0)
        self.rem_sel_btn = gtk.Button("Remove Selected")
        self.rem_all_btn = gtk.Button("Remove All")
        self.rem_box.pack_start(self.rem_sel_btn, False, True, 0)
        self.rem_box.pack_start(self.rem_all_btn, False, True, 0)
        # create box to hold selection buttons
        self.sel_box = gtk.HBox(True, 0)
        self.sel_inverse_btn = gtk.Button("Select Inverse")
        self.sel_all_btn = gtk.Button("Select All")
        self.sel_none_btn = gtk.Button("Select None")
        self.sel_box.pack_start(self.sel_inverse_btn, False, True, 0)
        self.sel_box.pack_start(self.sel_all_btn, False, True, 0)
        self.sel_box.pack_start(self.sel_none_btn, False, True, 0)
        # create box to hold playlist options
        self.list_opts_box = gtk.HBox(True, 0)
        self.list_save_btn = gtk.Button("Save Playlist")
        self.list_load_btn = gtk.Button("Load Playlist")
        self.list_opts_box.pack_start(self.list_save_btn, False, True, 0)
        self.list_opts_box.pack_start(self.list_load_btn, False, True, 0)
        # add each box to the notebook
        self.notebook.append_page(self.cli_box, None)
        self.notebook.append_page(self.add_box, None)
        self.notebook.append_page(self.rem_box, None)
        self.notebook.append_page(self.sel_box, None)
        self.notebook.append_page(self.list_opts_box, None)
        self.notebook.set_tab_label_text(self.cli_box, 'CLI')
        self.notebook.set_tab_label_text(self.add_box, 'Add')
        self.notebook.set_tab_label_text(self.rem_box, 'Remove')
        self.notebook.set_tab_label_text(self.sel_box, 'Select')
        self.notebook.set_tab_label_text(self.list_opts_box, "Playlist Opts.")
        # add everything so far to the bottom portion of the window
        self.bottom_box.pack_start(self.listbox, True, True, 0)
        self.bottom_box.pack_start(self.notebook, False, True, 0)
        
        # add the top and bottom boxes to the main content box
        self.content_box.pack_start(self.top_box, False, True, 0)
        self.content_box.pack_start(self.bottom_box, True, True, 0)
        
        # add the content box to the window.. we have a GUI!
        self.window.add(self.content_box)
        
    def setup_handlers(self):
        self.window.connect('destroy', self.on_window_close)
        
        self.status_icon.connect('activate', self.on_icon_click)
        self.status_icon.connect('popup-menu', self.on_icon_right_click, self.menu)
        
        self.menu_item_show.connect('activate', self.on_show_click, self.status_icon)
        self.menu_item_quit.connect('activate', self.on_quit_click, self.status_icon)
        
        self.audio_slider.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.audio_slider.connect('button_press_event', self.on_slider_click)
        
        self.play_btn.connect('clicked', self.on_play_click)
        self.stop_btn.connect('clicked', self.on_stop_click)
        self.previous_btn.connect('clicked', self.on_previous_click)
        self.next_btn.connect('clicked', self.on_next_click)
        self.repeat_btn.connect('clicked', self.on_repeat_click)
        self.shuffle_btn.connect('clicked', self.on_shuffle_click)
        self.volume_btn.connect('value_changed', self.on_volume_change)
        
        self.listbox.connect('row_activated', self.on_audio_click)
        # TODO: add listener for cli
        self.add_file_btn.connect('clicked', self.on_add_file_click)
        self.add_folder_btn.connect('clicked', self.on_add_folder_click)
        self.rem_sel_btn.connect('clicked', self.on_remove_selected_click)
        self.rem_all_btn.connect('clicked', self.on_remove_all_click)
        self.sel_inverse_btn.connect('clicked', self.on_select_inverse_click)
        self.sel_all_btn.connect('clicked', self.on_select_all_click)
        self.sel_none_btn.connect('clicked', self.on_select_none_click)
        self.list_save_btn.connect('clicked', self.on_list_save_click)
        self.list_load_btn.connect('clicked', self.on_list_load_click)
      
    def show(self):
        self.window.show_all()
        self.listbox.show()

