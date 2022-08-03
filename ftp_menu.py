#————————————————————————————————————————————————————————————————————————
#   FTP MENU class
#
import const
from helper_func import clear_screen
import getpass

class FTP_Menu:
    import os

    #————————————————————————————————————————————————————————————————
    #   SHORT PATH NAME

    def _short_path_name(self, fullpath):
        p = self.os.path.basename(self.os.path.normpath(fullpath))
        if p == '':
            p = '/'
        return p
    
    #————————————————————————————————————————————————————————————————
    #   POPULATE ITEMS

    def populate_items(self, ftp):

        # The menu is a list. Each menu item comprises a 1-based index,
        # ID, display name, and list of flags.

        self.items = []
        i = 1
        # Special case for disconnected state
        if ftp._ftp == None:
            self.items.append((i, const.kMenuID_connect, 'Connect...', ()))
            i += 1
            self.items.append((i, const.kMenuID_connect_rand, 'Connect to random...', ()))
            i += 1
        else:
            self.items.append((i, const.kMenuID_disconnect, f'Disconnect from {ftp._url}', ()))
            i += 1
            
        # Local options
        self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))
        loc_dir = self._short_path_name(self.os.getcwd())
        self.items.append((0, const.kMenuID_loc_label, f'LOCAL: {loc_dir}', (const.kMenuFlag_disabled)))
        self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))
        self.items.append((i, const.kMenuID_loc_list, 'List files and directories...', ()))
        i+=1
        self.items.append((i, const.kMenuID_loc_cwd, 'Go to directory...', ()))
        i+=1
        self.items.append((i, const.kMenuID_loc_ren, 'Rename...', ()))
        i+=1
        self.items.append((i, const.kMenuID_loc_mkdir, 'New directory...', ()))
        i+=1
        self.items.append((i, const.kMenuID_loc_rm, 'Delete...', ()))
        i+=1
        self.items.append((i, const.kMenuID_loc_search, 'Search for a file...', ()))
        i+=1

        # Remote options
        if ftp._ftp != None:
            self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))
            rem_dir = self._short_path_name(ftp.rem_dir())
            self.items.append((0, const.kMenuID_rem_label, f'REMOTE: {rem_dir}', (const.kMenuFlag_disabled)))
            self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))
            self.items.append((i, const.kMenuID_rem_list, 'List files and directories', ()))
            i += 1
            self.items.append((i, const.kMenuID_rem_cwd, 'Go to directory...', ()))
            i += 1
            self.items.append((i, const.kMenuID_rem_ren, 'Rename...', ()))
            i+=1
            self.items.append((i, const.kMenuID_rem_mkdir, 'New directory...', ()))
            i += 1
            self.items.append((i, const.kMenuID_rem_rm, 'Delete...', ()))
            i += 1
            self.items.append((i, const.kMenuID_rem_search, 'Search for a file...', ()))
            i += 1

            # File transfer operations
            self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))
            self.items.append((0, const.kMenuID_rem_label, f'TRANSFER: BETWEEN {loc_dir} AND {rem_dir} ', (const.kMenuFlag_disabled)))
            self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))
            self.items.append((i, const.kMenuID_upload, 'upload file(s)', ()))
            i+=1
            self.items.append((i, const.kMenuID_download , 'download file(s)', ()))
            i+=1


        self.items.append((0, const.kMenuID_separator, '-', (const.kMenuFlag_separator)))

        self.items.append((i, const.kMenuID_quit, 'Quit', ()))

    #————————————————————————————————————————————————————————————————
    #   DRAW

    def draw(self, ftp):

        # Populate the menu items
        self.populate_items(ftp)

        clear_screen()

        # Some useful ANSI escape codes for awesome terminal text
        kANSI_esc = '\u001b'
        kANSI_bold  = kANSI_esc + '[1m'
        kANSI_white_on_blue = kANSI_esc + '[38;5;15m' + kANSI_esc + '[48;5;4m'
        kANSI_gray = kANSI_esc + '[38;5;243m'
        kANSI_reset = kANSI_esc + '[0m'

        print(self._top_marge)
        print(f'{self._left_marge}                  ┌───────────────────────────┐                  ')
        print(
            f'{self._left_marge}┌─────────────────┤{kANSI_white_on_blue}     A G I L E   F T P     {kANSI_reset}├─────────────────┐')
        print(f'{self._left_marge}│                 └───────────────────────────┘                 │')
        print(f'{self._left_marge}│                                                               │')

        for item in self.items:
            separator = const.kMenuFlag_separator in item[const.kIndex_flags]
            dimmed = separator or const.kMenuFlag_disabled in item[const.kIndex_flags]
            if dimmed:
                num = '     '
            else:
                i = item[const.kIndex_index]
                num = f'{i:>4}: '

            if separator:
                title = '─' * 48 + '      '
            else:
                title = item[const.kIndex_name]
            s = f'{num}{title}'
            n = 59 - len(s)
            print(f'{self._left_marge}│    ', end='')
            if dimmed:
                print(kANSI_gray, end='')
            print(f'{s}{" " * n}', end='')
            if dimmed:
                print(kANSI_reset, end='')
            print('│')

        print(f'{self._left_marge}│                                                               │')
        print(f'{self._left_marge}│                                                               │')
        print(f'{self._left_marge}└───────────────────────────────────────────────────────────────┘')

    #————————————————————————————————————————————————————————————————
    #   SHOW ERROR
    
    def show_error(self, string):
        clear_screen()
        print(self._top_marge)
        print(self._left_marge + '┌─' + '─' * 70 + '─┐')
        print(self._left_marge + '│ ' + ' ' * 70 + ' │')
        print(self._left_marge + '│ ' + string + ' ' * (70 - len(string)) + ' │')
        print(self._left_marge + '│ ' + ' ' * 70 + ' │')
        print(self._left_marge + '└─' + '─' * 70 + '─┘')
        print()
        self.get_input('Press Return to continue > ')

    #————————————————————————————————————————————————————————————————
    #   SHOW LIST
    
    def show_list(self, lines):
        print()
        # Would be nice to paginate this, allow scrolling, or whatever.
        for l in lines:
            print(self._left_marge + l)
        print()

    #————————————————————————————————————————————————————————————————
    #   SHOW LINE

    def show_line(self, line):
        print(self._left_marge + line)
    
    #————————————————————————————————————————————————————————————————
    #   GET INPUT

    def get_input(self, prompt, private=False):
        if private:
            return getpass.getpass(prompt=self._left_marge+prompt)
        else:
            return input(self._left_marge + prompt)
        
    #————————————————————————————————————————————————————————————————
    #   GET CHOICE

    def get_choice(self):
        s = self.get_input('        Selection > ')

        # Special case so we can quit with the Q key
        if s.lower() == 'q':
            return const.kMenuID_quit

        try:
            num = int(s)
            for item in self.items:
                if item[const.kIndex_index] == num:
                    return item[const.kIndex_id]
        except:
            return None

        return None

    #————————————————————————————————————————————————————————————————
    #   GET FTP URL

    def get_ftp_url(self):
        print()
        url = self.get_input('FTP site address > ')
        return url

    #————————————————————————————————————————————————————————————————
    #   GET USERNAME

    def get_username(self):
        print()
        return self.get_input('Enter username (or press Enter for anonymous) > ')

    #————————————————————————————————————————————————————————————————
    #   GET PASSWORD
    def get_password(self):
        print()
        return self.get_input('Enter password > ', private=True)

    #————————————————————————————————————————————————————————————————
    #   INITIALIZER

    def __init__(self):
        self._left_marge = ' ' * const.kMargin_left  # just a layout convenience
        self._top_marge = '\n' * const.kMargin_top

        self._url = None
        self._ftp = None
        self.name = None
        self.password = None
