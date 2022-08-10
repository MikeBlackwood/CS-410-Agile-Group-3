# ————————————————————————————————————————————————————————————————————————
#   AGILE FTP class
#
#   We really want to move this into another module. Just working in the
#   main.py file for now though.

import os
import random
from helper_func import readable_size_string
import ftplib
import fnmatch


class AgileFTP:
    from ftplib import FTP
    # ————————————————————————————————————————————————————————————————
    #   INIT

    def __init__(self, url=None, ftp=None):
        '''
            Initialize everything to a safe starting point. There's no
            concept of a saved state, to pick up in the next session,
            for now.
        '''
        self._url = url
        self._ftp = ftp
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

    def connect(self, url=None, port='21', username=None, password=None):
        success = False
        if url == None:
            url = self.random_ftp_server()
        
        try:
            try:
                port = int(port)
            except:
                port = 21
            self._ftp = self.FTP()
            self._ftp.connect(url, port)
            self._ftp.login(username, password)
            self._url = url
            
            success = True
            # Switch to binary mode to avoid file corruption and so we
            # can get file sizes (unsupported in ASCII mode).
            self._ftp.sendcmd("TYPE I")
        except:
            self._ftp = None
            self._url = None

        return success

    # ————————————————————————————————————————————————————————————————
    #   DISCONNECT

    def disconnect(self):
        if self._ftp != None:
            value = self._ftp.quit()
            self._ftp = None
            self._url = None
            return value
        if self._ftp == None:
            return 'Not connected'

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
        try:
            result = self._ftp.nlst(dfile)
            return result == [dfile]
        except:
            return False
    
    #————————————————————————————————————————————————————————————————
    #   GET FILES
    #
    #   Download files
    
    def get_files(self, f):
        if (self.is_file(f)):
            with open(f, 'wb') as fd:
                self._ftp.retrbinary(f"RETR {f}", fd.write)
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
            s = self.size(path)
            if s == None:
                return True # If we couldn't get a size, it's (probably) a directory
            else:
                return False
        else:
            return os.path.isdir(path)

    #————————————————————————————————————————————————————————————————
    #   SIZE
    
    def size(self, path, remote=True):
        if remote:
            try:
                return self._ftp.size(path)
            except:
                return None
        else:
            return os.path.size(path)
            
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
            names = []
            def cb(name):
                names.append(name)
            self._ftp.retrlines('LIST', callback=cb)
            
            sizes = []
            for f in names:
                sizes.append(self.size(f)) # None if unknown or a directory
        else:
            names = os.listdir()
            sizes = [os.stat(f).st_size for f in names]
        
        if names==[]:
            result = ['(empty directory)']
        else:
            result = []
            names_sizes = [(names[i], sizes[i]) for i in range(len(names))]
            names_sizes = sorted(names_sizes, key=lambda y: y[0])
            names = [ns[0] for ns in names_sizes]
            sizes = [ns[1] for ns in names_sizes]
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
    #   SEARCH FOR A FILE

    def search_file(self, path, remote=True):
        if remote:
            if self.is_file(path):
                res = 1
            else:
                res = 0
        else:
            names = os.listdir()
            if path in names:
                res = 1 
            else:
                res = 0
        return res
