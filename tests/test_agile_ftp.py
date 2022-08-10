import ftplib
import unittest
from unittest import TestCase
from unittest.mock import patch
from agile_ftp import AgileFTP
import ftplib


class AgileFTPTests(unittest.TestCase):

    # TEST CONNECT FUNCTION
    def test_random_ftp_server(self):
        ftp = AgileFTP()
        self.assertTrue(ftp.random_ftp_server())

    @patch('ftplib.FTP', autospec=True)
    def test_connect_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.connect('localhost', username='mb', password='test'), "Returned True after Connection")
        mock_ftp_lib.login.assert_called_with('mb', 'test')

    @patch('ftplib.FTP', autospec=True)
    def test_connect_random(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.connect(), "Returned True connect anonymously")
        mock_ftp_lib.login.assert_called_with()


    # TEST DISCONNECT FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_disconnect_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.disconnect(), "Disconnected")
        mock_ftp_lib.quit.assert_called_once()


    # TEST REMOVE DIR
    @patch('ftplib.FTP', autospec=True)
    def test_rem_dir(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        returned_val = ftp.rem_dir()
        mock_ftp_lib.pwd.assert_called()
        self.assertTrue(returned_val, mock_ftp_lib.pwd.return_value())


    # TEST IS FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_is_file_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.is_file('hello')
        mock_ftp_lib.nlst.assert_called()
        self.assertFalse(return_val, "File with name is not found")

    @patch('ftplib.FTP', autospec=True)
    def test_is_file_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['hello']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.is_file('hello')
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, True, "File with name is not found")


    # TEST GET FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_get_files_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['hello', 'test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.get_files('test')
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, 1, "File with name is not found")

    @patch('ftplib.FTP', autospec=True)
    def test_get_file_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['hello', 'test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.get_files('test2')
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, 0, "File with name is not found")


    # TEST IS DIRECTORY FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_is_dir_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['hello', 'test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.get_files('test2')
        mock_ftp_lib.nlst.assert_called()
        assert False


    # TEST SIZE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_size_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = 1024
        ftp = AgileFTP('test', mock_ftp_lib)
        return_val = ftp.size('test')
        mock_ftp_lib.size.assert_called_with('test')
        self.assertIs(return_val, 1024, 'Did not return size')

    @patch('ftplib.FTP', autospec=True)
    def test_size_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.size.return_value = None
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.size('test')
        mock_ftp_lib.size.assert_called_with('test')
        self.assertIs(return_val, None, 'Did not return size')


    # TEST RENAME FILE
    @patch('ftplib.FTP', autospec=True)
    def test_rename_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.rename.return_value = 'RNTO test1'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.rename('test', 'test1')
        mock_ftp_lib.rename.assert_called_with('test', 'test1')
        self.assertIs(return_val, 'RNTO test1', 'Rename did not execute correctly')

    @patch('ftplib.FTP', autospec=True)
    def test_rename_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.rename.return_value = '3'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.rename('test', 'test1')
        self.assertIs(return_val, '3', 'Rename did not execute correctly')

    # TEST DELETE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_delete_file_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.delete.return_value = '250 Test'
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_value = ftp.delete('Test')
        mock_ftp_lib.delete.assert_called_with('Test')
        self.assertIs(return_value, '250 Test')

    # @patch('ftplib.FTP', autospec=True)
    # def test_delete_file_false(self, mock_ftp_constructor):
    #     mock_ftp_lib = mock_ftp_constructor.return_value
    #     mock_ftp_lib.resp = '500'
    #     ftp = AgileFTP('localhost', mock_ftp_lib)
    #     return_value = ftp.delete('Test')
    #     mock_ftp_lib.delete.assert_called_with('Test')
    #     self.assertIs(return_value, '400 Test')


    def test_get_file_list(self):
        assert False

    def test_upload_file(self):
        assert False

    def test_mkdir(self):
        assert False
    
    # TEST SEARCH FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_search_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.search_file('test', True)
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, 1, "File has been found")
    
    # TEST SEARCH FILE FUNCTION
    @patch('ftplib.FTP', autospec=True)
    def test_search_false(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        mock_ftp_lib.nlst.return_value = ['test']
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.search_file('test2', True)
        mock_ftp_lib.nlst.assert_called()
        self.assertIs(return_val, 0, "File with name is not found")


if __name__ == '__main__':
    unittest.main()
