import os

#————————————————————————————————————————————————————————————————————————
#   READABLE SIZE STRING
#
#   Gratuitous, yet sweet. Given a size in bytes, returns a nicely
#   formatted string to show the size to a human. Changes 123445232 to
#   '123.4 MB', for example.

def readable_size_string(bytes):
    TB = 1024 ** 4
    GB = 1024 ** 3
    MB = 1024 ** 2
    KB = 1024
    
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

#————————————————————————————————————————————————————————————————————————
#   FTP MENU class
#

# some constant definitions

kMargin_left        = 10
kMargin_top         = 3

# item duple offsets
kIndex_index        = 0
kIndex_id           = 1
kIndex_name         = 2
kIndex_flags        = 3

# Command IDs
# Connection management
kMenuID_connect     = 'connect'     # connect to FTP server by URL
kMenuID_connect_rand= 'connect_rand'# connect to random FTP server
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

    #————————————————————————————————————————————————————————————————
    #   CLEAR SCREEN

    def clear_screen(self):
        import os
        if os.name == 'nt':         # Windows
            _ = os.system('cls')
        elif os.name == 'posix':    # macOS and Linux
            _ = os.system('clear')
        else:
            pass                    # unrecognized system: just don't clear

    #————————————————————————————————————————————————————————————————
    #   POPULATE ITEMS
    
    def populate_items(self, ftp):
        import os
        
        # The menu is a list. Each menu item comprises a 1-based index,
        # ID, display name, and list of flags.
        
        self.items = []
        i = 1
        # Special case for disconnected state
        if ftp._ftp == None:
            self.items.append((i, kMenuID_connect, 'Connect to...', ()))
            i+=1
            self.items.append((i, kMenuID_connect_rand, 'Connect to random', ()))
            i+=1
        else:
            self.items.append((i, kMenuID_disconnect, f'Disconnect from {ftp._url}', ()))
            i+=1
        
        # Local options
        self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))
        loc_dir = os.path.basename(os.path.normpath(os.getcwd()))
        self.items.append((0, kMenuID_loc_label, f'LOCAL: {loc_dir}', (kMenuFlag_disabled)))
        self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))
        self.items.append((i, kMenuID_loc_list, 'List files...', ()))
        i+=1
        self.items.append((i, kMenuID_loc_cwd, 'Go to directory...', ()))
        i+=1
        self.items.append((i, kMenuID_loc_mkdir, 'New directory...', ()))
        i+=1
        self.items.append((i, kMenuID_loc_rm, 'Delete...', ()))
        i+=1

        # Remote options
        if ftp._ftp != None:
            self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))
            rem_dir = os.path.basename(os.path.normpath(ftp._ftp.pwd()))
            self.items.append((0, kMenuID_rem_label, f'REMOTE: {rem_dir}', (kMenuFlag_disabled)))
            self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))
            self.items.append((i, kMenuID_rem_list, 'List files and directories', ()))
            i+=1
            self.items.append((i, kMenuID_rem_cwd, 'Go to directory...', ()))
            i+=1
            self.items.append((i, kMenuID_rem_mkdir, 'New directory...', ()))
            i+=1
            self.items.append((i, kMenuID_rem_rm, 'Delete...', ()))
            i+=1
        
        self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))

        self.items.append((i, kMenuID_quit, 'Quit', ()))

    #————————————————————————————————————————————————————————————————
    #   DRAW
    
    def draw(self, ftp):
        
        # Populate the menu items
        self.populate_items(ftp)

        self.clear_screen()
        
        # Some useful ANSI escape codes for awesome terminal text
        kANSI_esc   = '\u001b'
        kANSI_bold  = kANSI_esc + '[1m'
        kANSI_white_on_blue = kANSI_esc + '[38;5;15m' + kANSI_esc + '[48;5;4m'
        kANSI_gray  = kANSI_esc + '[38;5;244m'
        kANSI_reset = kANSI_esc + '[0m'
        
        print(self._top_marge)
        print(self._left_marge +  '                  ┌───────────────────────────┐                  ')
        print(self._left_marge + f'┌─────────────────┤{kANSI_white_on_blue}     A G I L E   F T P     {kANSI_reset}├─────────────────┐')
        print(self._left_marge +  '│                 └───────────────────────────┘                 │')
        print(self._left_marge +  '│                                                               │')
        
        for item in self.items:
            is_separator = kMenuFlag_separator in item[kIndex_flags]
            dimmed = is_separator or kMenuFlag_disabled in item[kIndex_flags]
            if dimmed:
                num = '     '
            else:
                i = item[kIndex_index]
                num = f'{i:>4}: '
            
            if is_separator:
                title = '─' * 48 + '      '
            else:
                title = item[kIndex_name]
            s = f'{num}{title}'
            n = 59 - len(s)
            print(self._left_marge + '│    ', end='')
            if dimmed:
                print(kANSI_gray, end='')
            print(f'{s}{" "*n}', end='')
            if dimmed:
                print(kANSI_reset, end='')
            print('│')
            
        print(self._left_marge + '│                                                               │')
        print(self._left_marge + '│                                                               │')
        print(self._left_marge + '└───────────────────────────────────────────────────────────────┘')

    #————————————————————————————————————————————————————————————————
    #   INPUT
    
    def input(self):
        s = input(self._left_marge + '           Selection > ')
        
        # Special case so we can quit with the Q key
        if s.lower() == 'q':
            return kMenuID_quit
        
        try:
            num = int(s)
            for item in self.items:
                if item[kIndex_index] == num:
                    return item[kIndex_id]
        except:
            return None
        
        return None

    #————————————————————————————————————————————————————————————————
    #   SHOW ERROR
    
    def show_error(self, string):
        self.clear_screen()
        print(self._top_marge)
        print(self._left_marge + '┌─' + '─' * 70 + '─┐')
        print(self._left_marge + '│ ' + ' ' * 70 + ' │')
        print(self._left_marge + '│ ' + string + ' ' * (70 - len(string)) + ' │')
        print(self._left_marge + '│ ' + ' ' * 70 + ' │')
        print(self._left_marge + '└─' + '─' * 70 + '─┘')
        print()
        input(self._left_marge + 'Press Return to continue > ')

    #————————————————————————————————————————————————————————————————
    #   GET FTP URL
    
    def get_ftp_url(self):
        print()
        url = input(self._left_marge + 'FTP site address > ')
        return url
    
    #————————————————————————————————————————————————————————————————
    # LEFT MARGIN
    
    def left_margin(self):
        return self._left_marge
    
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
    #   Return True if connection is successful
    
    def connect(self, url=None):
        
        success = False
        if url == None:
            url = self.random_ftp_server()
        
        try:
            self._ftp = self.FTP(url)
            self._ftp.login()
            self._url = url
            success = True
        except:
            self._ftp = None
            self._url = None

        return success
        
    #————————————————————————————————————————————————————————————————
    #   DISCONNECT
    
    def disconnect(self):
        if self._ftp != None:
            self._ftp.quit()
            self._ftp = None
            self._url = None

    #————————————————————————————————————————————————————————————————
    #   IS DIR?
    
    def is_dir(self, path):
        data = []
        self._ftp.dir(path, data.append)
        for i,d in enumerate(data):
            print(f'{i}: {d}')
        return True

    #————————————————————————————————————————————————————————————————
    #   SET PATH

    def set_path(self, path, remote=True):
        import os
        if remote:
            self._ftp.cwd(path)
        else:
            os.chdir(path)
    
    #————————————————————————————————————————————————————————————————
    #   DELETE
    
    def delete(self, path, remote=True):
        if remote:
            # Is this a file or a directory?
            breakpoint()
            if self.is_dir(path):
                result = self._ftp.rmdir(path)
            else:
                result = self._ftp.delete(path)
        else:
            result = False # WRITEME
        return result
        
    #————————————————————————————————————————————————————————————————
    #   PRINT REMOTE FILES 

    def display_rem_files(self):
        for word in self._ftp.nlst():
            print(word)  
              
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
            url = menu.get_ftp_url()
            
            try:
                ftp.connect(url)
            except:
                print('Error. No luck.')
        
        elif id == kMenuID_connect_rand:
            ftp.connect(None)
        
        elif id == kMenuID_disconnect:
            ftp.disconnect()
        
        elif id == kMenuID_loc_list:
            print()
            print()
            flist = sorted(os.listdir())
            max_len = len(max(flist, key = len))
            for f in flist:
                stats = os.stat(f)
                size_str = readable_size_string(stats.st_size)
                print(menu.left_margin() + f, ' ' * (max_len + 1 - len(f)), '{: >8}'.format(size_str))
            print()
            input(menu.left_margin() + 'Press Return to continue > ')
        
        elif id == kMenuID_loc_cwd:
            print()
            print()
            path = input(menu.left_margin() + 'New path (or “..”) > ')
            try:
                ftp.set_path(path, remote = False)
            except:
                menu.show_error(f'Cannot move to {path}.')
        
        elif id == kMenuID_loc_mkdir:
            print()
            print()
            dir_name = input(menu.left_margin() + 'New directory name > ')
            menu.show_error(f'Ain’t wrote yet..')

        elif id == kMenuID_loc_rm:
            print()
            print()
            path = input(menu.left_margin() + 'File to remove > ')
            try:
                result = ftp.delete(path, remote = False)
            except:
                menu.show_error(f'Cannot delete {path}.')

        elif id == kMenuID_rem_list:
            print()
            print()
            ftp.display_rem_files()
            print()
            input(menu.left_margin() + 'Press Return to continue > ')
        
        elif id == kMenuID_rem_cwd:
            print()
            print()
            path = input(menu.left_margin() + 'New path (or “..”) > ')
            try:
                ftp.set_path(path, remote = True)
            except:
                menu.show_error(f'Cannot move to {path}.')

        elif id == kMenuID_rem_mkdir:
            print()
            print()
            dir_name = input(menu.left_margin() + 'New directory name > ')
        
        elif id == kMenuID_rem_rm:
            print()
            print()
            path = input(menu.left_margin() + 'File to remove > ')
            try:
                result = ftp.delete(path, remote = True)
            except:
                menu.show_error(f'Cannot delete {path}.')
            
        elif id == kMenuID_upload:
            print()
            print()
            input(menu.left_margin() + 'To be implemented > ')
        
        elif id == kMenuID_download:
            print()
            print()
            input(menu.left_margin() + 'To be implemented > ')
            # example: with open('README', 'wb') as fp:
            #              result = ftp.retrbinary('RETR README', fp.write)
        
        else:
            pass # unknown menu item

    menu.clear_screen()
