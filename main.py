import sys
import os

import const
from helper_func import clear_screen
from ftp_menu import FTP_Menu
from agile_ftp import AgileFTP


# Safe import, so we don't crash if keyring is not installed
try:
    import keyring
except:
    keyring = None


#————————————————————————————————————————————————————————————————————————
#   MAIN

def main():

    # set up our ftp client class
    ftp = AgileFTP()
    
    # get a menu and loop on it
    menu = FTP_Menu()
    done = False
    
    while not done:
    
        menu.draw(ftp)
        id = menu.get_choice()
        
        if id == const.kMenuID_quit:
            ftp.disconnect()
            done = True
        
        elif id == const.kMenuID_connect:
        
            url = menu.get_ftp_url()
            connected = False
            
            num_attempts = 0
            while not connected:
                num_attempts += 1
                try:
                    username = menu.get_username()
                    if username != '':

                        try:
                            password = keyring.get_password(url, username)
                        except:
                            password = None
                        if password == None:
                            password = menu.get_password()
                    else:
                        username = None
                        password = None
                    
                    if ftp.connect(url, username, password):
                        connected = True
                    if keyring is not None:
                        keyring.set_password(url, username, password)
                except:
                    menu.show_line('Error. No luck.')
                if not connected:
                    if num_attempts < 3:
                        menu.show_line('Unsuccessful.')
                    else:
                        menu.show_error(f'Three unsuccessful attempts. Time to quit.')
                        sys.exit()

        elif id == const.kMenuID_connect_rand:
            ftp.connect(None)
        
        elif id == const.kMenuID_disconnect:
            ftp.disconnect()
        
        elif id == const.kMenuID_loc_cwd or id == const.kMenuID_rem_cwd:
            is_remote = (id == const.kMenuID_rem_cwd)
            path = menu.get_input('New path (or “..”) > ')
            try:
                ftp.set_path(path, remote=is_remote)
            except:
                menu.show_error(f'Cannot move to {path}.')
        
        elif id == const.kMenuID_loc_ren or id == const.kMenuID_rem_ren:
            is_remote = (id == const.kMenuID_rem_ren)
            curr_name = menu.get_input('File to rename > ')
            new_name = menu.get_input('New name > ')
            try:
                ftp.rename(path, new_name, remote=is_remote)
            except:
                menu.show_error(f'Cannot rename “{curr_name}” to “{new_name}.”')
        
        elif id == const.kMenuID_loc_mkdir or id == const.kMenuID_rem_mkdir:
            is_remote = (id == const.kMenuID_rem_mkdir)
            dir_name = menu.get_input('New directory name > ')
            try:
               ftp.mkdir(dir_name, remote=is_remote)
            except:
               menu.show_error(f'Cannot make directory “{dir_name}”.')

        elif id == const.kMenuID_loc_rm or id == const.kMenuID_rem_rm:
            is_remote = (id == const.kMenuID_rem_rm)
            path = menu.get_input('File to remove > ')
            try:
                result = ftp.delete(path, remote=is_remote)
            except:
                menu.show_error(f'Cannot delete {path}.')

        elif id == const.kMenuID_loc_list or id == const.kMenuID_rem_list:
            is_remote = (id == const.kMenuID_rem_list)
            lines = ftp.get_file_list(remote=is_remote)
            menu.show_list(lines)
            menu.get_input('Press Return to continue > ')
        
        elif id == const.kMenuID_loc_search:
            path = menu.get_input('Name of the file to search > ')
            try: 
                res = ftp.search_loc_file(path)
                print('')
                if res == 1 :
                    menu.show_line(f'{path} has been found')
                    menu.get_input('Press Return to continue > ')
                else:
                    menu.show_error(f'Cannot find {path}.') 
            except:
                menu.show_error(f'Cannot find {path}.')


        elif id == const.kMenuID_upload:
            lines = ftp.get_file_list(remote=False)
            menu.show_list(lines)
            
            path = menu.get_input('File(s) to upload > ')
            path.strip(" ")
            files=path.split(',')
            try:
                for f in files:
                    res = ftp.upload_file(f)
                    if(res):
                        continue
                    else:
                        menu.show_error(f'Cannot find {f} in working directory.')
                        break
            except:
                menu.show_error(f'Cannot upload {path}.')
        
        elif id == const.kMenuID_download:
            path = menu.get_input('File(s) to  download > ')

            path.strip(" ")
            files = path.split(',')
            try:
                for f in files:
                    res=ftp.get_files(f)
                    if(res):
                        continue
                    else:
                        menu.show_error(f'Cannot find {f} in working directory.')
                        break
            except:
                menu.show_error(f'Cannot download {path}.')

        else:
            pass # unknown menu item

    clear_screen()

#————————————————————————————————————————————————————————————————————————

if __name__ == '__main__':
    main()
