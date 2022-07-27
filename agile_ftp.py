# ————————————————————————————————————————————————————————————————————————
#   AGILE FTP class
#
#   We really want to move this into another module. Just working in the
#   main.py file for now though.

import random

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

    def connect(self, url=None):

        success = False
        if url == None:
            url = self.random_ftp_server()

        try:
            self._ftp = self.FTP(url)
            self.name = self.name
            self._ftp.login()
            self._url = url
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

    # ————————————————————————————————————————————————————————————————
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
