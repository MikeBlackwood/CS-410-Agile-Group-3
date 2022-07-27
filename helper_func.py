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

