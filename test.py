import unittest
from unittest.mock import patch, mock_open, MagicMock
import local_system
from virtual_system import File, Directory, FileSystem

class TestFile(unittest.TestCase):

    def setUp(self):
        self.file = File("test.txt", "This is a test file.")

    def test_file_initialization(self):
        self.assertEqual(self.file.name, "test.txt")
        self.assertEqual(self.file.content, "This is a test file.")
        self.assertEqual(self.file.size, len("This is a test file."))

class TestDirectory(unittest.TestCase):

    def setUp(self):
        self.directory = Directory("test_dir", 755)

    def test_directory_initialization(self):
        self.assertEqual(self.directory.name, "test_dir")
        self.assertEqual(self.directory.permissions, 755)
        self.assertEqual(self.directory.files, [])
        self.assertEqual(self.directory.subdirs, [])

class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.fs = FileSystem()

    def test_change_working_directory(self):
        new_dir = Directory("new_dir", 755)
        self.fs.change_working_directory(new_dir)
        self.assertEqual(self.fs.current_directory, new_dir)

    def test_create_directory(self):
        new_dir = self.fs.create_directory("new_dir")
        self.assertIn(new_dir, self.fs.current_directory.subdirs)

    def test_create_file(self):
        new_file = self.fs.create_file("new_file.txt", "This is a new file.")
        self.assertIn(new_file, self.fs.current_directory.files)

    def test_chmod(self):
        new_file = self.fs.create_file("new_file.txt", "This is a new file.")
        self.fs.chmod("777", "new_file.txt")
        self.assertEqual(new_file.permissions, 0o777)




class TestLocalSystem(unittest.TestCase):

    @patch('os.listdir')
    def test_ls(self, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'dir1']
        local_system.local_execute_command('ls')
        mock_listdir.assert_called_once()

    @patch('os.chdir')
    def test_cd(self, mock_chdir):
        local_system.local_execute_command('cd dir1')
        mock_chdir.assert_called_once_with('dir1')

    @patch('os.mkdir')
    def test_mkdir(self, mock_mkdir):
        local_system.local_execute_command('mkdir new_dir')
        mock_mkdir.assert_called_once_with('new_dir')

    @patch('shutil.rmtree')
    def test_rmdir(self, mock_rmtree):
        local_system.local_execute_command('rmdir dir1')
        mock_rmtree.assert_called_once_with('dir1')

    @patch('os.remove')
    def test_rm(self, mock_remove):
        local_system.local_execute_command('rm file1.txt')
        mock_remove.assert_called_once_with('file1.txt')

    @patch('builtins.open', new_callable=mock_open)
    def test_touch(self, mock_file):
        local_system.local_execute_command('touch new_file.txt')
        mock_file.assert_called_once_with('new_file.txt', 'w')

    @patch('builtins.open', new_callable=mock_open, read_data='Hello World')
    def test_cat(self, mock_file):
        local_system.local_execute_command('cat file1.txt')
        mock_file.assert_called_once_with('file1.txt', 'r')

    @patch('os.getcwd')
    def test_pwd(self, mock_getcwd):
        mock_getcwd.return_value = '/home/user'
        local_system.local_execute_command('pwd')
        mock_getcwd.assert_called_once()

    # ... add more tests for other commands ...

if __name__ == "__main__":
    unittest.main()
