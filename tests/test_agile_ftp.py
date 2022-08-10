import ftplib
import unittest
from unittest import TestCase
from unittest.mock import patch
from agile_ftp import AgileFTP
import ftplib


class AgileFTPTests(unittest.TestCase):

    # TEST RANDOM FTP SERVER FUNCTION
    def test_random_ftp_server(self):
        ftp = AgileFTP()
        self.assertTrue(ftp.random_ftp_server())

    # TEST CONNECT FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_connect_manual(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.connect(url='testserver'), "Connected")
        mock_ftp_lib.login.assert_called_with(None, None)

    # TEST CONNECT FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_connect_random(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.connect(None), "Connected")
        mock_ftp_lib.login.assert_called_with(None, None)

    # TEST DISCONNECT FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_disconnect(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.disconnect(), "Disconnected")
        mock_ftp_lib.quit.assert_called_once()

    # TEST REMOTE DIR
    @patch('ftplib.FTP', autospec=True)
    def test_rem_dir(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        returned_val = ftp.rem_dir()
        mock_ftp_lib.pwd.assert_called()
        self.assertTrue(returned_val, mock_ftp_lib.pwd.return_value())

    # TETST IS FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_is_file_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.is_file('test'), "File was found")
        mock_ftp_lib.nlst.assert_called()

    # TEST IS FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_is_file_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertFalse(ftp.is_file('test'), "File was not found")
        mock_ftp_lib.nlst.assert_called()

    # TEST GET FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_get_files_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.get_files('test')
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, 1, "File was downloaded")

    # TEST GET FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_get_file_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.get_files('test2')
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, 0, "File could not be downloaded")

    # TEST IS DIRECTORY FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_is_dir_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = None
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.is_dir('test', True)
        mock_ftp_lib.size.assert_called_with('test')
        self.assertIs(return_val, True, "It is a directory")

    # TEST IS DIRECTORY FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_is_dir_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = 1024
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.is_dir('test', True)
        mock_ftp_lib.size.assert_called_with('test')
        self.assertIs(return_val, False, "It is not a directory")

    # TEST SIZE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_size_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = 1024
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.size('test')
        mock_ftp_lib.size.assert_called_with('test')
        self.assertIs(return_val, 1024, "Size was returned")

    # TEST SIZE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_size_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = None
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.size('test')
        mock_ftp_lib.size.assert_called_with('test')
        self.assertIs(return_val, None, "No size value to return")

    # TEST SET PATH
    @patch('ftplib.FTP', autospec=True)
    def test_set_path(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        ftp.set_path('test')
        mock_ftp_lib.cwd.assert_called_with('test')
        
    # TEST RENAME FILE
    @patch('ftplib.FTP', autospec=True)
    def test_rename(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        ftp.rename('test', 'test1')
        mock_ftp_lib.rename.assert_called_with('test', 'test1')

    # TEST DELETE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_delete_dir(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = None
        mock_ftp_lib.rmd.return_value = 'ret_val'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_value = ftp.delete('test')
        mock_ftp_lib.rmd.assert_called_with('test')
        self.assertIs(return_value, 'ret_val', "Directory was deleted")

    # TEST DELETE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_delete_file(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = 1024
        mock_ftp_lib.delete.return_value = 'ret_val'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_value = ftp.delete('test')
        mock_ftp_lib.delete.assert_called_with('test')
        self.assertIs(return_value, 'ret_val', "File was deleted")

    # TEST GET FILE LIST FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_get_file_list(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.retrlines.return_value = 'test'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        ftp.get_file_list('test')
        mock_ftp_lib.retrlines.assert_called()

    # TEST UPLOAD FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_upload_file_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.storbinary.return_value = 'test'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_value = ftp.upload_file('test')
        mock_ftp_lib.storbinary.assert_called()
        self.assertIs(return_value, 1, "File was uploaded")

    # TEST UPLOAD FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_upload_file_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.storbinary.return_value = 'test'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_value = ftp.upload_file('test2')
        self.assertIs(return_value, 0, "File could not be uploaded")

    # TEST MAKE DIRECTORY FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_mkdir(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.mkd.return_value = 'test'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        ftp.mkdir('test')
        mock_ftp_lib.mkd.assert_called_with('test')

    # TEST SEARCH FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_search_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.search_file('test', True)
        mock_ftp_lib.nlst.assert_called_with('test')
        self.assertIs(return_val, 1, "File has been found")
    
    # TEST SEARCH FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_search_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.search_file('test2', True)
        mock_ftp_lib.nlst.assert_called_with('test2')
        self.assertIs(return_val, 0, "File with name is not found")

if __name__ == '__main__':
    unittest.main()
