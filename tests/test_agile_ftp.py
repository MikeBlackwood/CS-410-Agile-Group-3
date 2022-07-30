import ftplib
import unittest
from unittest.mock import patch
from agile_ftp import AgileFTP
import ftplib

class AgileFTPTests(unittest.TestCase):


    def test_random_ftp_server(self):
        ftp = AgileFTP()
        self.assertTrue(ftp.random_ftp_server())

    @patch('ftplib.FTP', autospec=True)
    def test_connect_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.connect('localhost', 'mb', 'test'), "Returned True after Connection")
        mock_ftp_lib.login.assert_called_with('mb', 'test')

    @patch('ftplib.FTP', autospec=True)
    def test_connect_random(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.connect(), "Returned True connect anonemusly")
        mock_ftp_lib.login.assert_called_with('mb', 'test')

    @patch('ftplib.FTP', autospec=True)
    def test_disconnect_true(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        self.assertTrue(ftp.disconnect(), "Disconnected")
        mock_ftp_lib.quit.assert_called_once()

    @patch('ftplib.FTP', autospec=True)
    def test_rem_dir(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        returned_val = ftp.rem_dir()
        mock_ftp_lib.pwd.assert_called()
        self.assertTrue(returned_val, mock_ftp_lib.pwd.return_value())

    @patch('ftplib.FTP', autospec=True)
    def test_is_file(self, mock_ftp_constructor):
        mock_ftp_lib = mock_ftp_constructor.return_value
        ftp = AgileFTP('localhost', mock_ftp_lib)
        return_val = ftp.is_file('hello')
        mock_ftp_lib.nlst.assert_called()
        self.assertFalse(return_val, "File with name is not found")


    def test_get_files_true(self):
        assert False


    def test_get_file_false(self):
        assert False

    def test_is_dir(self):
        assert False


    def test_rename(self):
        assert False


    def test_delete(self):
        assert False


    def test_get_file_list(self):
        assert False


    def test_upload_file(self):
        assert False


    def test_mkdir(self):
        assert False



if __name__ == '__main__':
    unittest.main()