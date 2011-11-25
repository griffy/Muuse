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

def format_time(seconds):
    time = ''
    if seconds >= 3600:
        hours = seconds / 3600
        seconds = seconds - (hours * 3600)
        time = str(hours) + ':'

    if seconds >= 600:
        minutes = seconds / 60
        seconds = seconds - (minutes * 60)
        time += str(minutes) + ':'
    elif seconds >= 60:
        minutes = seconds / 60
        seconds = seconds - (minutes * 60)
        time += '0' + str(minutes) + ':'
    else:
        time += '00:'

    if seconds > 9:
        time += str(seconds)
    else:
        time += '0' + str(seconds)
    return time
