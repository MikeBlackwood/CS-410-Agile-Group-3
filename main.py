  
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

    import os
    
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
        # The menu is a list. Each menu item comprises a 1-based index,
        # ID, display name, and list of flags.
        
        self.items = []
        i = 1
        # Special case for disconnected state
        if ftp._ftp == None:
            self.items.append((i, kMenuID_connect, 'Connect...', ()))
            i+=1
            self.items.append((i, kMenuID_connect_rand, 'Connect to random...', ()))
            i+=1
        # Local options
        else:
            self.items.append((i, kMenuID_disconnect, f'Disconnect from {ftp._url}', ()))
            i+=1
            self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))
            loc_dir = self.os.path.basename(self.os.path.normpath(ftp._loc_path))
            self.items.append((0, kMenuID_loc_label, f'LOCAL: {loc_dir}', (kMenuFlag_disabled)))
            self.items.append((0, kMenuID_separator, '-', (kMenuFlag_separator)))
            self.items.append((i, kMenuID_loc_list, 'List files', ()))
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
            rem_dir = self.os.path.basename(self.os.path.normpath(ftp._rem_path))
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
        kANSI_white_on_blue = kANSI_esc + '[38;5;15m' + kANSI_esc + '[48;5;4m'
        kANSI_gray  = kANSI_esc + '[38;5;244m'
        kANSI_reset = kANSI_esc + '[0m'
        
        print(self._top_marge)
        print(f'{self._left_marge}                  ┌───────────────────────────┐                  ')
        print(f'{self._left_marge}┌─────────────────┤{kANSI_white_on_blue}     A G I L E   F T P     {kANSI_reset}├─────────────────┐')
        print(f'{self._left_marge}│                 └───────────────────────────┘                 │')
        print(f'{self._left_marge}│                                                               │')
        
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
            print(f'{self._left_marge}│    ', end='')
            if dimmed:
                print(kANSI_gray, end='')
            print(f'{s}{" "*n}', end='')
            if dimmed:
                print(kANSI_reset, end='')
            print('│')
            
        print(f'{self._left_marge}│                                                               │')
        print(f'{self._left_marge}│                                                               │')
        print(f'{self._left_marge}└───────────────────────────────────────────────────────────────┘')

    #————————————————————————————————————————————————————————————————
    #   INPUT
    
    def input(self):
        s = input(f'{self._left_marge}        Selection > ')
        
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
        url = input(f'{self._left_marge}FTP site address > ')
        return url
    
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
    #   SET PATH

    def set_path(self, path, remote=True):
        if remote:
            self._ftp.cwd(path)
            self._rem_path = path
        else:
            pass # WRITEME
    
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
            print('[dummy output]')
            print('image1.png     zero bytes  Aug 5, 2019')
            print('image2.png       27 bytes  Sep 3, 2019')
            print('textfile.txt    301 KB     May 1, 2018')
            print('something.jpg   1.3 MB     Jan 3, 2011')
            print()
            input('Press Return to continue > ')
        
        elif id == kMenuID_loc_cwd:
            print()
            print()
            path = input('New path (or “..”) > ')
            try:
                result = ftp.cwd(path)
                ftp.set_path(path, remote = False)
            except:
                menu.show_error(f'Cannot move to {path}.')

        elif id == kMenuID_loc_mkdir:
            print()
            print()
            dir_name = input('New directory name > ')
            menu.show_error(f'Ain’t wrote yet..')

        elif id == kMenuID_loc_rm:
            print()
            print()
            path = input('File to remove > ')
        
        elif id == kMenuID_rem_list:
            print()
            print()
            ftp.display_rem_files()
            print()
            input('Press Return to continue > ')
            # example: result = ftp.retrlines('LIST')
        
        elif id == kMenuID_rem_cwd:
            print()
            print()
            path = input('New path (or “..”) > ')
            try:
                ftp.set_path(path, remote = True)
            except:
                menu.show_error(f'Cannot move to {path}.')

        elif id == kMenuID_rem_mkdir:
            print()
            print()
            dir_name = input('New directory name > ')
        
        elif id == kMenuID_rem_rm:
            print()
            print()
            path = input('File to remove > ')

        elif id == kMenuID_upload:
            print()
            print()
            input('To be implemented > ')
        
        elif id == kMenuID_download:
            print()
            print()
            input('To be implemented > ')
            # example: with open('README', 'wb') as fp:
            #              result = ftp.retrbinary('RETR README', fp.write)
        
        else:
            pass # unknown menu item

    menu.clear_screen()
