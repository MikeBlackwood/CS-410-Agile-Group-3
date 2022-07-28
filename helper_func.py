#————————————————————————————————————————————————————————————————————————
#   CLEAR SCREEN
#

def clear_screen():
    import os
    if os.name == 'nt':         # Windows
        _ = os.system('cls')
    elif os.name == 'posix':    # macOS and Linux
        _ = os.system('clear')
    else:
        pass                    # unrecognized system: just don't clear


#————————————————————————————————————————————————————————————————————————
#   READABLE SIZE STRING
#
#   Gratuitous, yet sweet. Given a size in bytes, returns a nicely
#   formatted string to show the size to a human. Changes 123445232 to
#   '123.4 MB', for example.

def readable_size_string(bytes):
    TB = 1000 ** 4
    GB = 1000 ** 3
    MB = 1000 ** 2
    KB = 1000
    
    if bytes == KB:
        return 'no bytes'
    elif bytes < KB:
        return f'{bytes}  B'
    elif bytes < MB:
        return '{:.1f}'.format(bytes / KB) + ' KB'
    elif bytes < GB:
        return '{:.1f}'.format(bytes / MB) + ' MB'
    elif bytes < TB:
        return '{:.1f}'.format(bytes / GB) + ' GB'
    else:
        return '{:.1f}'.format(bytes / TB) + ' TB'

