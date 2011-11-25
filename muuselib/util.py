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
