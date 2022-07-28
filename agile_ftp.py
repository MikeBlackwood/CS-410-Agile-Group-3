# ————————————————————————————————————————————————————————————————————————
#   AGILE FTP class
#
#   We really want to move this into another module. Just working in the
#   main.py file for now though.

import os
import random
from helper_func import readable_size_string

class AgileFTP:
    from ftplib import FTP

    # ————————————————————————————————————————————————————————————————
    #   RANDOM FTP SERVER
    #
    #   Pick a random FTP server from a short list of public sites

    def random_ftp_server(self):
        return random.choice(self._public_ftp_urls)

    # ————————————————————————————————————————————————————————————————
    #   CONNECT
    #
    #   If called with url=None, ask the user for an FTP server URL.
    #   Return True if connection is successful

    def connect(self, url=None, username=None, password=None):
        
        success = False
        if url == None:
            url = self.random_ftp_server()
        
        try:
            self._ftp = self.FTP(url)
            self._ftp.login(username, password)
            self._url = url
            success = True
        except:
            self._ftp = None
            self._url = None

        return success

    # ————————————————————————————————————————————————————————————————
    #   DISCONNECT

    def disconnect(self):
        if self._ftp != None:
            self._ftp.quit()
            self._ftp = None
            self._url = None

    #————————————————————————————————————————————————————————————————
    #   REM_DIR
    
    def rem_dir(self):
        wd = self._ftp.pwd()
        return self._ftp.pwd()
    
    #————————————————————————————————————————————————————————————————
    #   IS FILE
    #
    #   Function to check if the given file exists or not
    
    def is_file(self,dfile):
        names = self._ftp.nlst()
        if dfile in names:
            return True
        else:
            return False
    
    #————————————————————————————————————————————————————————————————
    #   GET FILES
    #
    #   Download files
    
    def get_files(self, f):
        if (self.is_file(f)):
            with open(f, 'wb') as fd:
                total = self._ftp.size(f)
                with tqdm(total=total, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    def cb(data):
                        pbar.update(len(data))
                        fd.write(data)
                self._ftp.retrbinary('RETR {}'.format(f), cb)
            res=1
        else:
            res=0
            
        return res
        
    #————————————————————————————————————————————————————————————————
    #   IS DIR?
    
    def is_dir(self, path, remote):
    
        if remote:
            #
            # DEBUG: It's possible that some FTP servers will return a size
            # for folders. I don't think the correct behavior is specified.
            # If that's the case, we'll need some other method to determine
            # whether something is a folder. For example, we might try to
            # read the contents of the directory—if it works, it's a folder.
            # (But the converse is not necessarily true: if it doesn't work,
            # it may be a permissions violation or some other issue. That said,
            # if you can't read the contents of a folder, you probably
            # shouldn't be able to delete it! So that might be okay.
            #
            try:
                self._ftp.size(path)
            except:
                return True  # If we couldn't get a size, it's a directory
        else:
            return os.path.isdir(path)
        
        return False

    #————————————————————————————————————————————————————————————————
    #   SET PATH

    def set_path(self, path, remote=True):
        import os
        if remote:
            self._ftp.cwd(path)
        else:
            os.chdir(path)
    
    #————————————————————————————————————————————————————————————————
    #   RENAME
    
    def rename(self, old_name, new_name, remote=True):
        if remote:
            self._ftp.rename(old_name, new_name)
        else:
            os.rename(old_name, new_name)
            
    #————————————————————————————————————————————————————————————————
    #   DELETE
    
    def delete(self, path, remote=True):
        if remote:
            # Is this a file or a directory?
            if self.is_dir(path, remote):
                result = self._ftp.rmdir(path)
            else:
                result = self._ftp.delete(path)
        else:
            result = os.delete(path)
            
        return result
        
    #————————————————————————————————————————————————————————————————
    #   GET FILE LIST
    #
    #   Return a list of strings, each of which describes one file,
    #   for display.
    
    def get_file_list(self, remote=True):
        if remote:
            names = self._ftp.nlst()
            sizes = []
            for f in names:
                try:
                    sizes.append(self._ftp.size(f))
                except:
                    sizes.append(None) # Directories [generally] have no size
        else:
            names = os.listdir()
            sizes = [os.stat(f).st_size for f in names]
        
        if names==[]:
            result = ['(empty directory)']
        else:
            result = []
            names = sorted(names)
            longest_name = max(names, key=len)
            max_len = len(longest_name)
            
            for i,f in enumerate(names):
                if sizes[i] == None:
                    size_str = ''
                else:
                    size_str = readable_size_string(sizes[i])
                result.append(f + ' ' * (max_len + 1 - len(f)) + '{: >8}'.format(size_str))
        
        return result
    
    #————————————————————————————————————————————————————————————————
    #   PUT FILE ONTO REMOTE SERVERE

    def upload_file(self,path):
        
        names = os.listdir()
        if path in names:
            with open(path, "rb") as file:
                self._ftp.storbinary(f"STOR {path}", file)
            res = 1
        else:
            res = 0
        return res

    #————————————————————————————————————————————————————————————————
    #   CREATE NEW DIRECTORY
    def mkdir(self, dir_name, remote=True):
        if remote:
            self._ftp.mkd(dir_name)
        else:
            os.mkdir(dir_name)

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
