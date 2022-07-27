import const
from helper_func import clear_screen
from ftp_menu import FTP_Menu
from agile_ftp import AgileFTP
#————————————————————————————————————————————————————————————————————————
#   CLEAR SCREEN

clear_screen()

#————————————————————————————————————————————————————————————————————————
#   AGILE FTP class
#
#   We really want to move this into another module. Just working in the
#   main.py file for now though.



if __name__ == '__main__':
    # set up our ftp client class
    ftp = AgileFTP()
    
    # get a menu and run it once

    menu = FTP_Menu()
    done = False
    
    while not done:
        menu.draw(ftp)
        id = menu.input()
        if id == const.kMenuID_quit:
            ftp.disconnect()
            done = True
        
        elif id == const.kMenuID_connect:
            url = menu.get_ftp_url()
            name = menu.get_user_name()
            password = menu.get_passwod()

            try:
                ftp.connect(url)
                ftp.login()
            except:
                print('Error. No luck.')
        
        elif id == const.kMenuID_connect_rand:
            ftp.connect(None)
        
        elif id == const.kMenuID_disconnect:
            ftp.disconnect()
        
        elif id == const.kMenuID_loc_list:
            print()
            print()
            print('[dummy output]')
            print('image1.png     zero bytes  Aug 5, 2019')
            print('image2.png       27 bytes  Sep 3, 2019')
            print('textfile.txt    301 KB     May 1, 2018')
            print('something.jpg   1.3 MB     Jan 3, 2011')
            print()
            input('Press Return to continue > ')
        
        elif id == const.kMenuID_loc_cwd:
            print()
            print()
            path = input('New path > ')
            # example: result = ftp.cwd('debian')
        
        elif id == const.kMenuID_loc_mkdir:
            print()
            print()
            dir_name = input('New directory name > ')
        
        elif id == const.kMenuID_loc_rm:
            print()
            print()
            path = input('File to remove > ')
        
        elif id == const.kMenuID_rem_list:
            print()
            print()
            print('[dummy output]')
            print('image1.png     zero bytes  Aug 5, 2019')
            print('image2.png       27 bytes  Sep 3, 2019')
            print('textfile.txt    301 KB     May 1, 2018')
            print('something.jpg   1.3 MB     Jan 3, 2011')
            print()
            input('Press Return to continue > ')
            # example: result = ftp.retrlines('LIST')
        
        elif id == const.kMenuID_rem_cwd:
            print()
            print()
            path = input('New path > ')
        
        elif id == const.kMenuID_rem_mkdir:
            print()
            print()
            dir_name = input('New directory name > ')
        
        elif id == const.kMenuID_rem_rm:
            print()
            print()
            path = input('File to remove > ')

        elif id == const.kMenuID_upload:
            print()
            print()
            input('To be implemented > ')
        
        elif id == const.kMenuID_download:
            print()
            print()
            input('To be implemented > ')
            # example: with open('README', 'wb') as fp:
            #              result = ftp.retrbinary('RETR README', fp.write)
        
        else:
            pass # unknown menu item

    clear_screen()
