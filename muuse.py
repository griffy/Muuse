import os

import gobject
import pygtk
pygtk.require('2.0')
import gtk
from pyap import playlist
from pyap.audio import extensions
from pyap.audio import Audio
from pyap.player import Player
from pyap.library import Library
from pyap.playlist import Playlist

from muusewindow import MuuseWindow
from muuselib.image import get_icon
from muuselib.util import format_time

class Muuse(MuuseWindow):
    def __init__(self):
        MuuseWindow.__init__(self)
        
        self.player = Player()
        self.player.connect('audio_ended', self.on_audio_end)

        self.library = Library()

        self.playlists = {}
        
        audio_list = self.library.all_audio()
        self.playlists['library'] = Playlist('Library', audio_list)

        # we want to see the library to start with
        self.set_playlist_view('library')
        
        self.show()
        
    def set_playlist_view(self, playlist):
        self._playlist_view = playlist
        self.listbox.clear()
        self.extend_listbox(self.playlists[playlist])
        # in case the repeat state was changed in a previous playlist,
        # make sure the button matches the state for this playlist
        self.set_repeat(self.playlists[playlist].get_repeat())
        # same for shuffle
        self.set_shuffle(self.playlists[playlist].is_shuffling())
        # only the library playlist is persistent
        if playlist == 'library':
            #self.playlist_listbox.hide()
            #self.library_listbox.show()
            # (re)enable all buttons affecting library
            self.add_file_btn.set_sensitive(True)
            self.add_folder_btn.set_sensitive(True)
            self.rem_sel_btn.set_sensitive(True)
            self.rem_all_btn.set_sensitive(True)
            self.sel_inverse_btn.set_sensitive(True)
            self.sel_all_btn.set_sensitive(True)
            self.sel_none_btn.set_sensitive(True)
            self.list_load_btn.set_sensitive(True)
            self.list_save_btn.set_sensitive(True)
        else:
            #self.library_listbox.hide()
            #self.playlist_listbox.show()
            # disable all buttons that affect the library
            self.add_file_btn.set_sensitive(False)
            self.add_folder_btn.set_sensitive(False)
            self.rem_sel_btn.set_sensitive(False)
            self.rem_all_btn.set_sensitive(False)
            self.sel_inverse_btn.set_sensitive(False)
            self.sel_all_btn.set_sensitive(False)
            self.sel_none_btn.set_sensitive(False)
            self.list_load_btn.set_sensitive(False)
            self.list_save_btn.set_sensitive(False)

    def playlist_view(self):
        return self._playlist_view
      
    def current_playlist(self):
        return self.playlists[self.playlist_view()]
         
    def extend_listbox(self, audio_list):
        text_list = [str(audio) for audio in audio_list]
        self.listbox.extend(text_list)
        
    def extend_library(self, audio_list):
        self.playlists['library'].extend(audio_list)
        self.library.add_audio(audio_list)
        if self.playlist_view() == 'library':
            self.extend_listbox(audio_list)

    def set_repeat(self, state):
        self.current_playlist().set_repeat(state)
        if state == playlist.REPEAT_ALL:
            self.repeat_btn.set_image(get_icon('repeatall'))
        elif state == playlist.REPEAT_ONE:
            self.repeat_btn.set_image(get_icon('repeatone'))
        elif state == playlist.REPEAT_OFF:
            self.repeat_btn.set_image(get_icon('repeatoff'))

    def set_shuffle(self, shuffling):
        self.current_playlist().set_shuffle(shuffling)
        if shuffling:
            self.shuffle_btn.set_image(get_icon('shuffleon'))
        else:
            self.shuffle_btn.set_image(get_icon('shuffleoff'))
            
    def set_volume(self, volume):
        self.player.set_volume(volume)
        if volume >= 0.7:
            self.volume_btn.set_image(get_icon('volumemax'))
        elif volume >= 0.3:
            self.volume_btn.set_image(get_icon('volumemid'))
        else:
            self.volume_btn.set_image(get_icon('volumemin'))
            
    def pause(self):
        self.player.pause()
        self.play_btn.set_image(get_icon('play'))
        self.status_icon.set_tooltip(u'Paused: %s' % self.player.current_audio())
        
    def resume(self):
        self.player.resume()
        self.play_btn.set_image(get_icon('pause'))
        self.status_icon.set_tooltip(u'Playing: %s' % self.player.current_audio())
        
    def play(self, audio, focus=False):
        self.player.stop()
        index = self.current_playlist().current_index
        self.listbox.select_and_scroll(index, focus)
        self.audio_label.set_text(str(audio))
        self.status_icon.set_tooltip(u'Playing: %s' % audio)
        update_progress = self.progress_updater()
        gobject.timeout_add(250, update_progress.next)
        self.player.play(audio)
        self.play_btn.set_image(get_icon('pause'))

    def stop(self):
        self.player.stop()
        self.audio_label.set_text('')
        self.status_icon.set_tooltip('Muuse')
        self.play_btn.set_image(get_icon('play'))
        self.audio_slider.set_fraction(0)
        self.audio_slider.set_text('')
        
    def progress_updater(self):
        position = self.player.position()
        duration = self.player.audio_duration()
        while position < duration:
            pos_fmt = format_time(position)
            dur_fmt = format_time(duration)
            self.audio_slider.set_fraction(position * 1.0 / duration)
            self.audio_slider.set_text("%s / %s" % (pos_fmt, dur_fmt))
            position = self.player.position()
            duration = self.player.audio_duration()
            yield True
        yield False
        
    def on_window_close(self, *arg, **kwargs):
        gtk.main_quit()

    def on_icon_click(self, *args, **kwargs):
        if self.window.props.visible:
            self.window.hide()
        else:
            self.window.show()   
                  
    def on_icon_right_click(self, *args, **kwargs):
        if 'data' in kwargs:
            menu.popup(self.menu, None, None, 3, args[2])
        
    def on_show_click(self, *args, **kwargs):
        if self.window.props.visible:
            self.window.hide()
        else:
            self.window.show()
        
    def on_quit_click(self, *args, **kwargs):
        gtk.main_quit()
        
    def on_audio_end(self, audio):
        next_audio = self.current_playlist().next()
        if next_audio:
            self.play(next_audio, focus=True)
            
    def on_slider_click(self, widget, event, **kwargs):
        audio_duration = self.player.audio_duration()
        if audio_duration:
            slider_width = self.audio_slider.get_allocation()[2]
            seek_time = event.x / slider_width * audio_duration
            self.player.set_position(seek_time)  
        
    def on_play_click(self, *args, **kwargs):
        if self.player.is_playing():
            self.pause()
        elif self.player.is_paused():
            self.resume()
        else:
            # the user manually selected a song to play
            index = self.listbox.get_selected_row()
            playlist = self.current_playlist()
            playlist.current_index = index
            self.play(playlist[index], focus=False)
                
    def on_stop_click(self, *args, **kwargs):
        self.stop()
			
    def on_previous_click(self, *args, **kwargs):
        audio = self.current_playlist().previous()
        if audio:
		    self.play(audio)
			
    def on_next_click(self, *args, **kwargs):
        audio = self.current_playlist().next()
        if audio:
		    self.play(audio)
              
    def on_repeat_click(self, *args, **kwargs):
        # Order by click: NO_REPEAT, REPEAT_ONE, REPEAT_ALL
        if self.current_playlist().is_repeating_one():
            self.set_repeat(playlist.REPEAT_ALL)
        elif self.current_playlist().is_repeating_all():
            self.set_repeat(playlist.REPEAT_OFF)
        else:
            self.set_repeat(playlist.REPEAT_ONE)
            
    def on_shuffle_click(self, *args, **kwargs):
        self.set_shuffle(not self.current_playlist().is_shuffling())
        
    def on_volume_change(self, widget, value):
        self.set_volume(value)

    def on_audio_click(self, widget, path, *args, **kwargs):
        index = path[0]
        playlist = self.current_playlist()
        playlist.current_index = index
        self.play(playlist[index], focus=False)   
            
    # TODO: handle playlist files
    def on_add_file_click(self, *args, **kwargs):
        dialog = gtk.FileChooserDialog("Select File(s)", 
                                       None, 
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL,
                                        gtk.RESPONSE_CANCEL, 
                                        gtk.STOCK_OPEN,
                                        gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_select_multiple(True)
        
        filter = gtk.FileFilter()
        filter.set_name('Audio')
        for ext in extensions.AUDIO:
            filter.add_pattern('*.%s' % ext)
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            uris = dialog.get_filenames()
            audio_list = [Audio(uri) for uri in uris]
            self.extend_library(audio_list)
        dialog.destroy()
       
    def on_add_folder_click(self, widget, data=None):
        dialog = gtk.FileChooserDialog("Select Folder(s)", 
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                       (gtk.STOCK_CANCEL,
                                        gtk.RESPONSE_CANCEL, 
                                        gtk.STOCK_OPEN,
                                        gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_select_multiple(True)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            uris = []
            folders = dialog.get_filenames()
            for folder in folders:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        ext = os.path.splitext(file)[1].replace('.', '')
                        if ext in extensions.AUDIO:
                            uri = os.path.join(root, file)
                            uris.append(uri)
            audio_list = [Audio(uri) for uri in uris]
            self.extend_library(audio_list)
        dialog.destroy()
        
    # TODO
    def on_remove_selected_click(self, *args, **kwargs):
        pass
        
    # TODO
    def on_remove_all_click(self, *args, **kwargs):
        pass
        
    def on_select_inverse_click(self, *args, **kwargs):
        self.listbox.select_inverse()
        
    def on_select_all_click(self, *args, **kwargs):
        self.listbox.select_all()

    def on_select_none_click(self, *args, **kwargs):
        self.listbox.unselect_all()
        
    def on_list_save_click(self, *args, **kwargs):
        dialog = gtk.FileChooserDialog("Save Playlist", 
                                       None, 
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, 
                                        gtk.RESPONSE_CANCEL, 
                                        gtk.STOCK_SAVE,
                                        gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            uri = dialog.get_filename()
            # FIXME: it's not that simple
            self.current_playlist().export('m3u', uri)
        dialog.destroy()

    def on_list_load_click(self, *args, **kwargs):
        dialog = gtk.FileChooserDialog("Load Playlist", 
                                       None, 
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, 
                                        gtk.RESPONSE_CANCEL, 
                                        gtk.STOCK_OPEN,
                                        gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        
        filter = gtk.FileFilter()
        filter.set_name('Playlists')
        for ext in extensions.PLAYLIST:
            filter.add_pattern('*.%s' % ext)
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            uri = dialog.get_filename()
            playlist = import_playlist(uri)
            self.playlists[str(playlist)] = playlist
        dialog.destroy()
			
    def main(self):
        gtk.main()
			
if __name__ == "__main__":
	muuse = Muuse()
	muuse.main()
