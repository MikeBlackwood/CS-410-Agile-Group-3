import const
import logging 
import os
import sys
from agile_ftp import AgileFTP
from helper_func import clear_screen
from ftp_menu import FTP_Menu



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
    
    # set up logging 
    logging.basicConfig(
        filename='history.log', 
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        encoding='utf-8', 
        level=logging.DEBUG)
    logging.info('====FTP client started====')   

    # get a menu and loop on it
    menu = FTP_Menu()
    done = False
    
    while not done:
    
        menu.draw(ftp)
        id = menu.get_choice()
        
        # Quit
        if id == const.kMenuID_quit:
            ftp.disconnect()
            done = True
            logging.info('====FTP client quit====') 
        
        # Connect to FTP
        elif id == const.kMenuID_connect:
            # User may optionally enter a port number after a ':'
            (url, port) = menu.get_ftp_url()
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
                    
                    if ftp.connect(url=url, port=port, username=username, password=password):
                        connected = True
                        logging.info('Connect to FTP server - Sucessfully connected')
                    if keyring is not None:
                        keyring.set_password(url, username, password)
                except:
                    menu.show_line('Error. No luck.')
                if not connected:
                    if num_attempts < 3:
                        menu.show_line('Unsuccessful.')
                        logging.info('Connect to FTP server - Wrong info entered')
                    else:
                        menu.show_error(f'Three unsuccessful attempts. Time to quit.')
                        logging.info('Connect to FTP server - Wrong info entered')
                        logging.info('Connect to FTP server - Three failed attempts')
                        sys.exit()

        # Connect to random 
        elif id == const.kMenuID_connect_rand:
            ftp.connect(None)
            logging.info('Connect to random FTP server')
        
        # Disconnect
        elif id == const.kMenuID_disconnect:
            ftp.disconnect()
            logging.info('Disconnect from FTP server')
        
        # Change directory 
        elif id == const.kMenuID_loc_cwd or id == const.kMenuID_rem_cwd:
            is_remote = (id == const.kMenuID_rem_cwd)
            path = menu.get_input('New path (or “..”) > ')
            try:
                ftp.set_path(path, remote=is_remote)
                logging.info('Moved to %s', path)
            except:
                menu.show_error(f'Cannot move to {path}.')
                logging.info('Failed to move to %s', path)
        
        # Rename directory 
        elif id == const.kMenuID_loc_ren or id == const.kMenuID_rem_ren:
            is_remote = (id == const.kMenuID_rem_ren)
            curr_name = menu.get_input('File to rename > ')
            new_name = menu.get_input('New name > ')
            try:
                ftp.rename(path, new_name, remote=is_remote)
                logging.info('Renamed %s to %s', curr_name, new_name)
            except:
                menu.show_error(f'Cannot rename “{curr_name}” to “{new_name}.”')
                logging.info('Failed to rename %s to %s', curr_name, new_name)
        
        # Make directory
        elif id == const.kMenuID_loc_mkdir or id == const.kMenuID_rem_mkdir:
            is_remote = (id == const.kMenuID_rem_mkdir)
            dir_name = menu.get_input('New directory name > ')
            try:
               ftp.mkdir(dir_name, remote=is_remote)
               logging.info('Made new directory: %s', dir_name)
            except:
               menu.show_error(f'Cannot make directory “{dir_name}”.')
               logging.info('Failed to make new directory: %s', dir_name)

        # Remove directory directory or file 
        elif id == const.kMenuID_loc_rm or id == const.kMenuID_rem_rm:
            is_remote = (id == const.kMenuID_rem_rm)
            path = menu.get_input('File to remove > ')
            try:
                result = ftp.delete(path, remote=is_remote)
                logging.info('Deleted %s', path)
            except:
                menu.show_error(f'Cannot delete {path}.')
                logging.info('Failed to delete %s', path)

        # List directory 
        elif id == const.kMenuID_loc_list or id == const.kMenuID_rem_list:
            is_remote = (id == const.kMenuID_rem_list)
            lines = ftp.get_file_list(remote=is_remote)
            menu.show_list(lines)
            logging.info('Listed files')
            menu.get_input('Press Return to continue > ')
            
        
        # Search for a file
        elif id == const.kMenuID_loc_search or id == const.kMenuID_rem_search:
            is_remote = (id == const.kMenuID_rem_search)
            path = menu.get_input('Name of the file to search > ')
            try: 
                res = ftp.search_file(path,remote=is_remote)
                print('')
                if res == 1 :
                    menu.show_line(f'{path} has been found')
                    logging.info('Search for and found %s', path)
                    menu.get_input('Press Return to continue > ')
                else:
                    menu.show_error(f'Cannot find {path}.') 
                    logging.info('Searched for and did not find %s', path)
            except:
                menu.show_error(f'Cannot find {path}.')

        # Upload 
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
                        logging.info('Uploaded %s', f)
                        continue
                    else:
                        menu.show_error(f'Cannot find {f} in working directory.')
                        logging.info('Failed to upload %s, no such file', f)
                        break
            except:
                menu.show_error(f'Cannot upload {path}.')
        
        #Download
        elif id == const.kMenuID_download:
            path = menu.get_input('File(s) to  download > ')

            path.strip(" ")
            files = path.split(',')
            try:
                for f in files:
                    res=ftp.get_files(f)
                    if(res):
                        logging.info('Downloaded %s', f)
                        continue
                    else:
                        menu.show_error(f'Cannot find {f} in working directory.')
                        logging.info('Failed to download %s, no such file', f)
                        break
            except:
                menu.show_error(f'Cannot download {path}.')

        # Unkown menu item
        else:
            logging.info('Unknown menu item')
            pass 

    clear_screen()

#————————————————————————————————————————————————————————————————————————

if __name__ == '__main__':
    main()
