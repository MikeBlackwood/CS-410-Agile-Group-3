  
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
#   FTP MENU class
#

# some constant definitions

kMargin_left        = 10
kMargin_top         = 3

# item duple offsets
kIndex_id           = 0
kIndex_name         = 1
kIndex_flags        = 2

# Command IDs
# Connection management
kMenuID_connect     = 'connect'     # connect to FTP server URL
kMenuID_disconnect  = 'disconnect'  # disconnect from FTP server
# Local directory operations
kMenuID_loc_label   = 'LOCAL'       # just a label
kMenuID_loc_list    = 'loc_list'    # list files in local working directory
kMenuID_loc_cwd     = 'loc_cwd'     # change local working directory
kMenuID_loc_mkdir   = 'loc_mkdir'   # create local directory
kMenuID_loc_rm      = 'loc_rm'      # delete local file or directory
# Remote directory operations
kMenuID_rem_label   = 'REMOTE'      # just a label
kMenuID_rem_list    = 'rem_list'    # list files in remote working directory
kMenuID_rem_cwd     = 'rem_cwd'     # change remote working directory
kMenuID_rem_mkdir   = 'rem_mkdir'   # create remote directory
kMenuID_rem_rm      = 'rem_rm'      # delete remote file or directory
# File transfer operations
kMenuID_upload      = 'upload'      # upload file(s)
kMenuID_download    = 'download'    # download file(s)
# Other
kMenuID_separator   = '---'         # NOP
kMenuID_quit        = 'quit'        # terminate this crazy app

kMenuFlag_disabled  = 'disabled'
kMenuFlag_separator = 'separator'


class FTP_Menu:

    import os

    #————————————————————————————————————————————————————————————————
    #   POPULATE ITEMS
    
    def populate_items(self, ftp):
        # The menu is a list. Each menu item comprises an ID, a display name,
        # and a list of flags.
        
        self.items = []
        # Special case for disconnected state
        if ftp._ftp == None:
            self.items.append((kMenuID_connect, 'Connect...', ()))
        else:
            self.items.append((kMenuID_disconnect, f'Disconnect from {ftp._url}', ()))
            self.items.append((kMenuID_separator, '-', (kMenuFlag_separator)))
            loc_dir = self.os.path.basename(self.os.path.normpath(ftp._loc_path))
            self.items.append((kMenuID_loc_label, f'LOCAL: {loc_dir}', (kMenuFlag_disabled)))
            self.items.append((kMenuID_separator, '-', (kMenuFlag_separator)))
            self.items.append((kMenuID_loc_list, 'List files', ()))
            self.items.append((kMenuID_loc_cwd, 'Go to directory...', ()))
            self.items.append((kMenuID_loc_mkdir, 'New directory...', ()))
            self.items.append((kMenuID_loc_rm, 'Delete...', ()))
        
        if ftp._ftp != None:
            self.items.append((kMenuID_separator, '-', (kMenuFlag_separator)))
            rem_dir = self.os.path.basename(self.os.path.normpath(ftp._rem_path))
            self.items.append((kMenuID_rem_label, f'REMOTE: {rem_dir}', (kMenuFlag_disabled)))
            self.items.append((kMenuID_separator, '-', (kMenuFlag_separator)))
            self.items.append((kMenuID_loc_list, 'List files', ()))
            self.items.append((kMenuID_loc_cwd, 'Go to directory...', ()))
            self.items.append((kMenuID_loc_mkdir, 'New directory...', ()))
            self.items.append((kMenuID_loc_rm, 'Delete...', ()))
        
        self.items.append((kMenuID_separator, '-', (kMenuFlag_separator)))

        self.items.append((kMenuID_quit, 'Quit', ()))
        
    #————————————————————————————————————————————————————————————————
    #   DRAW
    
    def draw(self, ftp):
        
        # Populate the menu items
        self.populate_items(ftp)

        clear_screen()
        
        # Some useful ANSI escape codes for awesome terminal text
        kANSI_gray  = '\u001b[38;5;243m'
        kANSI_reset = '\u001b[0m'
        
        print(self._top_marge)
        print(f'{self._left_marge}                ┌───────────────────────────┐')
        print(f'{self._left_marge}                │     A G I L E   F T P     │')
        print(f'{self._left_marge}                └───────────────────────────┘')
        print()
        print()
        
        for i,item in enumerate(self.items):
            separator = kMenuFlag_separator in item[kIndex_flags]
            dimmed = separator or kMenuFlag_disabled in item[kIndex_flags]
            if dimmed:
                print(kANSI_gray, end='')
            if dimmed:
                num = '   '
            else:
                num = f'{i+1:>2}:'
            
            if separator:
                title = '————————————————————————————————————————————————————'
            else:
                title = item[kIndex_name]
            print(f'{self._left_marge}{num} {title}')

            if dimmed:
                print(kANSI_reset, end='')
        print()
        
    #————————————————————————————————————————————————————————————————
    #   INPUT
    
    def input(self):
        s = input(f'{self._left_marge}Selection > ')
        try:
            i = int(s) - 1
        except:
            i = None
        if i != None and i in range(len(self.items)):
            return self.items[i][kIndex_id]
        else:
            return None
        
    #————————————————————————————————————————————————————————————————
    #   INITIALIZER
    
    def __init__(self):
        self._left_marge = ' ' * kMargin_left     # just a layout convenience
        self._top_marge = '\n' * kMargin_top
        
        self._url = None
        self._ftp = None
        
#————————————————————————————————————————————————————————————————————————
#   AGILE FTP class
#
#   We really want to move this into another module. Just working in the
#   main.py file for now though.

import random

class AgileFTP:
    
    from ftplib import FTP
    
    #————————————————————————————————————————————————————————————————
    #   RANDOM FTP SERVER
    #
    #   Pick a random FTP server from a short list of public sites
    
    def random_ftp_server(self):
        return random.choice(self._public_ftp_urls)
    
    #————————————————————————————————————————————————————————————————
    #   CONNECT
    #
    #   If called with url=None, ask the user for an FTP server URL.
    
    def connect(self, url=None):
        
        if url == None:
            url = random_ftp_server()
        
        try:
            self._ftp = self.FTP(url)
            self._ftp.login()
            self._url = url
        except:
            self._ftp = None
            self._url = None

        pass
        
    #————————————————————————————————————————————————————————————————
    #   DISCONNECT
    
    def disconnect(self):
        if self._ftp != None:
            self._ftp.quit()
            self._ftp = None
            self._url = None
    
    #————————————————————————————————————————————————————————————————
    #   INIT
    
    def __init__(self):
        '''
            Initialize everything to a safe starting point. There's no
            concept of a saved state, to pick up in the next session,
            for now.
        '''
        self._url = None
        self._ftp = None
        self._loc_path = ''
        self._rem_path = ''

        # Some freely accessible FTP sites, from https://www.mmnt.net
        self._public_ftp_urls = ['ftp.us.debian.org',
                                 'ftp.coreftp.com',
                                 'ftp.be.debian.org',
                                 'ftp.menandmice.com',
                                 'ftp.integra-s.com',
                                 'tp.kernel.ee',
                                 'ftp3.za.freebsd.org',
                                 'ftp.notepager.net',
                                 'ftp.getright.com',
                                 'ftp.europeonline.net',
                                 'ftp.dungeoncrawl.org',
                                 'ftp.openusenet.org',
                                 'ftp.gps.caltech.edu',
                                 'ftp.cc.gatech.edu',
                                 'ftp.logitech.com',
                                 'ftp-archive.freebsd.org',
                                 'ftp.coreftp.com',
                                 ]

if __name__ == '__main__':
    # set up our ftp client class
    ftp = AgileFTP()
    
    # get a menu and run it once

    menu = FTP_Menu()
    done = False
    
    while not done:
        menu.draw(ftp)
        id = menu.input()
        if id == kMenuID_quit:
            ftp.disconnect()
            done = True
        
        elif id == kMenuID_connect:
            ftp.connect(ftp.random_ftp_server())
        
        elif id == kMenuID_disconnect:
            ftp.disconnect()
        
        elif id == kMenuID_loc_list:
            pass
        
        elif id == kMenuID_loc_cwd:
            pass
        
        elif id == kMenuID_loc_mkdir:
            pass
        
        elif id == kMenuID_loc_rm:
            pass
        
        elif id == kMenuID_rem_list:
            pass
        
        elif id == kMenuID_rem_cwd:
            pass
        
        elif id == kMenuID_rem_mkdir:
            pass
        
        elif id == kMenuID_rem_rm:
            pass

        elif id == kMenuID_upload:
            pass
        
        elif id == kMenuID_download:
            pass
        
        else:
            pass # unknown menu item

    clear_screen()
