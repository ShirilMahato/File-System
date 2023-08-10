import datetime


import time
import os
# from unit_test import *

MAX_FILENAME_LENGTH = 50
MAX_CONTENT_LENGTH = 100
MAX_FILES = 100
MAX_DIRS = 100


class File:
    def __init__(self, name, content='', permissions='644', parent=None):
        self.name = name
        self.content = content
        self.size = len(content)
        self.creation_time = time.time()
        self.modified_time = self.creation_time
        self.content = content
        self.permissions = permissions
        self.parent = parent

class Directory:
    def __init__(self, name, permissions, parent=None):
        self.name = name
        self.creation_time = time.time()
        self.files = []
        self.subdirs = []
        self.permissions = permissions
        self.parent = parent
        
class FileSystem:
    def __init__(self):
        self.root_directory = Directory("/", 755, None)
        self.current_directory = self.root_directory

    def change_working_directory(self, new_current_directory):
        self.current_directory = new_current_directory

    def change_to_subdirectory(self, sub_dir_name):
        for subdir in self.current_directory.subdirs:
            if subdir.name == sub_dir_name:
                self.current_directory = subdir
                return
        print(f"Sub-directory '{sub_dir_name}' not found in current directory.")

    def create_directory(self, name, parent=None):
        new_dir = Directory(name, 755, parent)
        self.current_directory.subdirs.append(new_dir)
        return new_dir

    def create_file(self, name, content):
        new_file = File(name, content, '644', self.current_directory)
        self.current_directory.files.append(new_file)
        return new_file

    def chmod(self, permissions, item_name):
        item = None
        for file in self.current_directory.files:
            if file.name == item_name:
                item = file
                break
        if item is None:
            for subdir in self.current_directory.subdirs:
                if subdir.name == item_name:
                    item = subdir
                    break
        if item is not None:
            try:
                item.permissions = int(permissions, 8)
                print(f"Permissions of '{permissions}' changed to '{item_name}'.")
            except ValueError:
                print("Invalid permissions format.")
        else:
            print(f"Item '{item_name}' not found in the current directory.")

        
def add_file_to_directory(dir, file):
    for i in range(dir.file_count):
        if dir.files[i].name == file.name:
            print(f"File '{file.name}' already exists in the directory.")
            return
    if dir.file_count < MAX_FILES:
        dir.files.append(file)
        file.parent = dir
        dir.file_count += 1
    else:
        print("Directory is full. Cannot add file.")
    # def add_file_to_directory(dir, file):
    #     if len(dir.files) < MAX_FILES:
    #         dir.files.append(file)
    #     else:
    #         print("Directory is full. Cannot add file.")

    #     # Add the file to the current working directory in the file system
    #     fs.current_directory.files.append(file)

def add_directory_to_directory(parent_dir, sub_dir):
    for i in range(parent_dir.subdir_count):
        if parent_dir.subdirs[i].name == sub_dir.name:
            print(f"Directory '{sub_dir.name}' already exists in the parent directory.")
            return
    if parent_dir.subdir_count < MAX_DIRS:
        parent_dir.subdirs.append(sub_dir)
        sub_dir.parent = parent_dir
        parent_dir.subdir_count += 1
    else:
        print("Parent directory is full. Cannot add sub-directory.")




    def add_directory_to_directory(parent_dir, sub_dir):
        if len(parent_dir.subdirs) < MAX_DIRS:
            parent_dir.subdirs.append(sub_dir)
            sub_dir.parent = parent_dir

            # ANSI escape code for blue text
            blue_color = "\033[34m"
            # ANSI escape code to reset text color to default
            reset_color = "\033[0m"

            # Print the directory name in blue
            print(f"Added directory: {blue_color}{sub_dir.name}{reset_color} (Created: {time.ctime(sub_dir.creation_time)}, Permissions: {format_permissions(sub_dir.permissions, is_file=False)})")
        else:
            print("Parent directory is full. Cannot add sub-directory.")

        # Add the directory to the current working directory in the file system
        # fs.current_directory.subdirs.append(sub_dir)

        
    def create_directory(self, name, parent=None):
        new_dir = Directory(name, 755, parent)  # Default permissions set to 755
        self.current_directory.subdirs.append(new_dir)
        return new_dir

    def create_file(self, name, content):
        new_file = File(name, content, '', self.current_directory)
        self.current_directory.files.append(new_file)
        return new_file

    def chmod(self, permissions, item_name):
        item = None
        for file in self.current_directory.files:
            if file.name == item_name:
                item = file
                break
        if item is None:
            for subdir in self.current_directory.subdirs:
                if subdir.name == item_name:
                    item = subdir
                    break
        if item is not None:
            try:
                item.permissions = int(permissions, 8)
                print(f"Permissions of '{permissions}' changed to '{item_name}'.")
            except ValueError:
                print("Invalid permissions format.")
        else:
            print(f"Item '{item_name}' not found in the current directory.")
    
    def execute_command(self, command):
        command_parts = command.split()
        command_name = command_parts[0]
        arguments = command_parts[1:]

        if command_name == "mkdir":
            if len(arguments) > 0:
                permissions = 755
                if len(arguments) > 1:
                    try:
                        permissions = int(arguments[1])
                    except ValueError:
                        print("Invalid permissions. Using default permissions (755).")
                new_directory = Directory(arguments[0], permissions, self.current_directory)
                self.current_directory.subdirs.append(new_directory)
                print(f"Created directory: {new_directory.name}")
            else:
                print("Usage: mkdir <dir_name> [permissions]")

   

    def delete_file_from_directory(self, dir, file_name):
        for file in dir.files:
            if file.name == file_name:
                dir.files.remove(file)
                file_path = os.path.join(os.path.abspath(dir.name), file_name)  # Absolute path
                try:
                    os.remove(file_path) 
                    print(f"File '{file_name}' deleted from directory '{dir.name}'.")
                except OSError as e:
                    print(f"Error while deleting the file: {e}")
                    print(f"Failed to delete file '{file_name}' at path: {file_path}")
                break
        else:
            print(f"File '{file_name}' not found in the directory '{dir.name}'.")

    def delete_subdirectory_from_directory(self, dir, sub_dir_name):
        for sub_dir in dir.subdirs:
            if sub_dir.name == sub_dir_name:
                dir.subdirs.remove(sub_dir)
                dir_path = os.path.abspath(dir.name)  
                sub_dir_path = os.path.join(dir_path, sub_dir_name)  
                try:
                    os.rmdir(sub_dir_path)  
                    print(f"Directory '{sub_dir_name}' deleted from directory '{dir.name}'.")
                except OSError as e:
                    print(f"Error while deleting the directory: {e}")
                    print(f"Failed to delete directory '{sub_dir_name}' at path: {sub_dir_path}")
                break
        else:
            print(f"Sub-directory '{sub_dir_name}' not found in the directory '{dir.name}'.")

    def delete_file_and_sync(self, file_path):
        self.delete_file_from_file_system(file_path)  
        print("File deleted from actual file system.")

    def delete_directory_and_sync(self, dir_path):
        self.delete_directory_from_file_system(dir_path)  
        print("Directory deleted from actual file system.")


root_directory = Directory("/", 755, None)
current_directory = root_directory


def create_directory(self, name, parent=None):
        new_dir = Directory(name, 755, parent)  # Default permissions set to 755
        self.current_directory.subdirs.append(new_dir)
        return new_dir

def create_file(self, name, content):
    new_file = File(name, content, '', self.current_directory)
    self.current_directory.files.append(new_file)
    return new_file

def add_directory_to_directory(parent_dir, sub_dir):
    for existing_dir in parent_dir.subdirs:
        if existing_dir.name == sub_dir.name:
            print(f"Directory '{sub_dir.name}' already exists in the parent directory.")
            return

    parent_dir.subdirs.append(sub_dir)
    sub_dir.parent = parent_dir

def add_file_to_directory(dir, file):
    for existing_file in dir.files:
        if existing_file.name == file.name:
            print(f"File '{file.name}' already exists in the directory.")
            return

    dir.files.append(file)
    file.parent = dir


def delete_file_from_directory(dir, file_name):
    for file in dir.files:
        if file.name == file_name:
            dir.files.remove(file)
            break

def delete_subdirectory_from_directory(dir, sub_dir_name):
    for sub_dir in dir.subdirs:
        if sub_dir.name == sub_dir_name:
            dir.subdirs.remove(sub_dir)
            break

def copy_file_to_directory(source_file, target_dir, new_file_name):
    copied_file = File(new_file_name, source_file.content, source_file.permissions)
    add_file_to_directory(target_dir, copied_file)

def copy_directory_to_directory(source_dir, target_dir, new_sub_dir_name):
    copied_dir = Directory(new_sub_dir_name, source_dir.permissions, target_dir)
    for file in source_dir.files:
        copied_file = File(file.name, file.content, file.permissions)
        add_file_to_directory(copied_dir, copied_file)
    for subdir in source_dir.subdirs:
        copy_directory_to_directory(subdir, copied_dir, subdir.name)
    add_directory_to_directory(target_dir, copied_dir)

def move_file_to_directory(source_file, target_dir):
    delete_file_from_directory(source_file.parent, source_file.name)
    add_file_to_directory(target_dir, source_file)

def move_directory_to_directory(source_dir, target_dir):
    delete_subdirectory_from_directory(source_dir.parent, source_dir.name)
    add_directory_to_directory(target_dir, source_dir)


def list_directory_contents(dir, detailed):
    # ANSI escape code for blue text
    blue_color = "\033[34m"
    # ANSI escape code for white text
    white_color = "\033[37m"
    # ANSI escape code to reset text color to default
    reset_color = "\033[0m"

    print(f"Contents of directory '{dir.name}':")

    # Check if the directory has files or sub-directories
    has_items = len(dir.files) > 0 or len(dir.subdirs) > 0

    if not has_items:
        pass
    else:
        for file in dir.files:
            if detailed:
                permissions = format_permissions(file.permissions, is_file=True)
                print(f"File: {white_color}{file.name}{reset_color} (Size: {file.size} bytes, Created: {time.ctime(file.creation_time)}, Modified: {time.ctime(file.modified_time)}, Permissions: {permissions})")
            else:
                print(f"{white_color}{file.name}{reset_color}", end="  ")
        for subdir in dir.subdirs:
            if detailed:
                permissions = format_permissions(subdir.permissions, is_file=False)
                print(f"Sub-directory: {blue_color}{subdir.name}{reset_color} (Created: {time.ctime(subdir.creation_time)}, Permissions: {permissions})")
            else:
                print(f"{blue_color}{subdir.name}{reset_color}", end="  ")
    print()



def format_permissions(permissions, is_file):
    mapping = {7: "rwx", 6: "rw-", 5: "r-x", 4: "r--", 3: "-wx", 2: "-w-", 1: "--x", 0: "---"}
    permissions_str = ''.join(mapping[int(i)] for i in str(permissions))
    return ('-' if is_file else 'd') + permissions_str


def change_working_directory(new_current_directory):
    global current_directory
    current_directory = new_current_directory

def change_to_root_directory():
    global root_directory, current_directory
    current_directory = root_directory

def change_to_parent_directory():
    global current_directory
    if current_directory.parent is not None:
        current_directory = current_directory.parent
    else:
        print("Already in root directory.")

def change_to_subdirectory(sub_dir_name):
    global current_directory
    for subdir in current_directory.subdirs:
        if subdir.name == sub_dir_name:
            current_directory = subdir
            return
    print(f"Sub-directory '{sub_dir_name}' not found in current directory.")
    
def print_working_directory():
    global current_directory
    path = []
    dir = current_directory
    while dir is not root_directory:
        path.append(dir.name)
        dir = dir.parent

    path.append("/")
    path.reverse()

    print("Current working directory:", "/".join(path))


def find_file_in_directory(dir, file_name):
    for file in dir.files:
        if file.name == file_name:
            return file
    return None

def find_subdirectory_in_directory(dir, sub_dir_name):
    for subdir in dir.subdirs:
        if subdir.name == sub_dir_name:
            return subdir
    return None

def change_file_permissions(permissions, file):
    file.permissions = permissions
    print(f"File permissions for {permissions} changed to '{file.name}' .")

def change_directory_permissions(dir, permissions):
    dir.permissions = permissions
    print(f"Directory permissions for '{dir.name}' changed to {permissions}.")


    
def read_file_content(file):
    permissions_binary = int(str(file.permissions), 8)
    if permissions_binary & 4:  # Check if the file has read permission
        print(f"Content of file '{file.name}':\n{file.content}")
    else:
        print(f"Permission denied: Cannot read file '{file.name}'")

def append_file_content(file):
    permissions_binary = int(str(file.permissions or "755"), 8)
    if permissions_binary & 2:  # Check if the file has write permission
        print(f"Enter content to append to file '{file.name}'. Press Ctrl+z followed by enter in the new line to save and exit.")
        appended_content = []
        while True:
            try:
                line = input()
                if len(file.content) + len(line) + 1 <= MAX_CONTENT_LENGTH:  # +1 for the newline character
                    appended_content.append(line)
                else:
                    print(f"File '{file.name}' is full. Cannot append more content.")
            except EOFError:
                file.content += "\n" + "\n".join(appended_content)
                file.size = len(file.content)
                file.modified_time = time.time()
                print(f"\nContent appended to file '{file.name}'.")
                break
    else:
        print(f"Permission denied: Cannot append content to file '{file.name}'")

def edit_file_content(file):
    permissions_binary = int(str(file.permissions or "755"), 8)
    if permissions_binary & 2:  # Check if the file has write permission
        print(f"Enter new content for file '{file.name}'. Press Ctrl+z followed by enter in the new line to save and exit.")
        new_content = []
        while True:
            try:
                line = input()
                new_content.append(line)
            except EOFError:
                file.content = "\n".join(new_content)
                file.size = len(file.content)
                file.modified_time = time.time()
                print(f"\nContent of file '{file.name}' updated.")
                break
    else:
        print(f"Permission denied: Cannot edit file '{file.name}'")

def find_file_or_directory_in_directory(dir, name):
    for item in dir.files + dir.subdirs:
        if item.name == name:
            return item
    return None

def copy_file_or_directory_to_directory(source_item, target_dir, new_name):
    if isinstance(source_item, File):
        copied_file = File(new_name, source_item.content, source_item.permissions, target_dir)
        add_file_to_directory(target_dir, copied_file)
    elif isinstance(source_item, Directory):
        copied_dir = Directory(new_name, source_item.permissions, target_dir)
        for file in source_item.files:
            copied_file = File(file.name, file.content, file.permissions, copied_dir)
            add_file_to_directory(copied_dir, copied_file)
        for subdir in source_item.subdirs:
            copy_directory_to_directory(subdir, copied_dir, subdir.name)
        add_directory_to_directory(target_dir, copied_dir)

def move_file_or_directory_to_directory(source_item, target_dir):
    if isinstance(source_item, File):
        source_item.parent.files.remove(source_item)
        target_dir.files.append(source_item)
        source_item.parent = target_dir
    elif isinstance(source_item, Directory):
        source_item.parent.subdirs.remove(source_item)
        target_dir.subdirs.append(source_item)
        source_item.parent = target_dir

def save_project_to_system():
    answer = input("Do you want to save the project to the system? (y/n): ").lower()
    if answer == 'y':
        # Save the project to the system
        print("Saving project to the system...")
        # Your code to save the project to the system goes here
        print("Project saved to the system.")
    else:
        print("Project will not be saved to the system.")

def calculate_directory_size(directory):
    total_size = 0
    for file in directory.files:
        total_size += file.size
    for subdir in directory.subdirs:
        total_size += calculate_directory_size(subdir)
    return total_size

def du_command(directory):
    total_size = calculate_directory_size(directory)
    print(f"Total space used by '{directory.name}': {total_size} bytes")
    
def find_item(start_directory, name):
    results = []
    for file in start_directory.files:
        if file.name == name:
            results.append(file)
    for subdir in start_directory.subdirs:
        if subdir.name == name:
            results.append(subdir)
        results.extend(find_item(subdir, name))
    return results

def grep_pattern(directory, pattern):
    results = []
    for file in directory.files:
        lines = file.content.split("\n")
        for index, line in enumerate(lines):
            if pattern in line:
                results.append((file.name, index + 1, line))
    return results


def wc_file(file):
    lines = file.content.split("\n")
    words = file.content.split()
    characters = len(file.content)
    return len(lines), len(words), characters

def file_type(item):
    if isinstance(item, File):
        return "Regular file"
    elif isinstance(item, Directory):
        return "Directory"
    else:
        return "Unknown"
    
import zipfile

def zip_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in directory.files:
            zipf.writestr(file.name, file.content)
            
def unzip_to_directory(zip_name, directory):
    with zipfile.ZipFile(zip_name, 'r') as zipf:
        for name in zipf.namelist():
            content = zipf.read(name).decode()
            new_file = File(name, content, '', directory)
            directory.files.append(new_file)



COMMANDS = {
    "ls": "List directory contents. Use 'ls -l' for detailed view.",
    "mkdir": "Create a new directory. Usage: 'mkdir <dir_name> [permissions]'",
    "touch": "Create a new file. Usage: 'touch <file_name> [permissions]'",
    "rm": "Delete a file. Usage: 'rm <file_name>'",
    "rmdir": "Delete a directory. Usage: 'rmdir <dir_name>'",
    "cat": "Read file content. Usage: 'cat <file_name>'",
    "chmod": "Change file or directory permissions. Usage: 'chmod <file_or_dir_name> <permissions>'",
    "cd": "Change current directory. Use '..' to go up. Usage: 'cd <dir_name>'",
    "pwd": "Print current working directory.",
    "du": "Amount of spaces used by system.",
    "append": "Append content to a file. Usage: 'append <file_name>'",
    "edit": "Edit file content. Usage: 'edit <file_name>'",
    "cp":"copy file or directory in the same directory. Usage: 'cp <source_file_or_dir_name> <target_file_or_dir_name>'",
    "mv":"move file or directory in the same directory. Usage: 'mv <source_file_or_dir_name> <target_file_or_dir_name>'",
    "cpd": "Copy file or directory to another directory. Usage: 'cpd <source_file_or_dir_name> <target_dir_name>'",
    "mvd": "Move file or directory to another directory. Usage: 'mvd <source_file_or_dir_name> <target_dir_name>'",
    "clear": "Clear the terminal screen.",
    "cp": "Copy file or directory to another directory. Usage: 'cp <source_file_or_dir_name> <target_dir_name>'",
    "mv": "Move file or directory to another directory. Usage: 'mv <source_file_or_dir_name> <target_dir_name>'",
    "find": "find the files or directories. Usage: 'find <file_or_dir_name>'",
    "grep": "Find patterns in file. Usage: 'find <file_name> pattern'",
    "wc": "count lines, words, and characters in a file. Usage: 'wc <file_name>'",
    "file": "Display the file type. Usage: 'file <file_name>'",
    "exit": "Exit the program."
}

def execute_command(command, fs):
    global current_directory
    command_parts = command.split()
    command_name = command_parts[0]
    arguments = command_parts[1:]

    if command_name == "ls":
        list_directory_contents(current_directory, "-l" in arguments or "-la" in arguments or "-al" in arguments)
    elif command_name == "mkdir":
        if len(arguments) > 0:
            add_directory_to_directory(current_directory, fs.create_directory(arguments[0], current_directory))
        else:
            print("Usage: mkdir <dir_name>")


    elif command_name == "chmod":
        if len(arguments) > 1:
            try:
                permissions = int(arguments[1])
                if 0 <= permissions <= 777:
                    for file in current_directory.files:
                        if file.name == arguments[0]:
                            change_file_permissions(permissions,file)
                            break
                    else:
                        for subdir in current_directory.subdirs:
                            if subdir.name == arguments[0]:
                                change_directory_permissions(permissions,subdir)
                                break
                        else:
                            print(f"Item '{arguments[0]}' not found in the current directory.")
                else:
                    print("Invalid permissions. Please enter a number between 0 and 777.")
            except ValueError:
                print("Invalid permissions. Please enter a number between 0 and 777.")
        else:
                print("Usage: chmod <file_or_dir_name> <permissions>")



    elif command_name == "touch":
        if len(arguments) > 0:
            add_file_to_directory(current_directory, fs.create_file(arguments[0], ""))
        else:
            print("Usage: touch <file_name>")

    elif command_name == "rm":
        if len(arguments) > 0:
            delete_file_from_directory(current_directory, arguments[0])
        else:
            print("Usage: rm <file_name>")
    elif command_name == "rmdir":
        if len(arguments) > 0:
            delete_subdirectory_from_directory(current_directory, arguments[0])
        else:
            print("Usage: rmdir <dir_name>")
    elif command_name == "cat":
        if len(arguments) > 0:
            for file in current_directory.files:
                if file.name == arguments[0]:
                    read_file_content(file)
                    break
            else:
                print(f"File '{arguments[0]}' not found in the current directory.")
        else:
                print("Usage: cat <file_name>")

    elif command_name == "cd":
        if len(arguments) > 0:
            if arguments[0] == "..":
                change_to_parent_directory()
            else:
                change_to_subdirectory(arguments[0])
        else:
            change_to_root_directory()
    elif command_name == "pwd":
        print_working_directory()
        
    elif command_name == "append":
        if len(arguments) > 0:
            file = find_file_in_directory(current_directory, arguments[0])
            if file is not None:
                append_file_content(file)
            else:
                print(f"File '{arguments[0]}' not found in the current directory.")
        else:
            print("Usage: append <file_name>")
    elif command_name == "edit":
        if len(arguments) > 0:
            file = find_file_in_directory(current_directory, arguments[0])
            if file is not None:
                edit_file_content(file)
            else:
                print(f"File '{arguments[0]}' not found in the current directory.")
        else:
            print("Usage: edit <file_name>")

    elif command_name == "cp":
        if len(arguments) > 1:
            source_item = find_file_or_directory_in_directory(current_directory, arguments[0])
            target_dir = find_subdirectory_in_directory(current_directory, arguments[1])

            if source_item is not None and target_dir is not None:
                copy_file_or_directory_to_directory(source_item, target_dir, arguments[0])
            else:
                print("Source item or target directory not found.")
        else:
            print("Usage: cp <source_file_or_dir_name> <target_dir_name>")

    elif command_name == "mv":
        if len(arguments) > 1:
            source_item = find_file_or_directory_in_directory(current_directory, arguments[0])
            target_dir = find_subdirectory_in_directory(current_directory, arguments[1])

            if source_item is not None and target_dir is not None:
                move_file_or_directory_to_directory(source_item, target_dir)
            else:
                print("Source item or target directory not found.")
        else:
            print("Usage: mv <source_file_or_dir_name> <target_dir_name>")

    elif command_name == "du":
        du_command(current_directory)

    elif command_name == "clear":
        clear_screen()
        return
    
    elif command_name == "find":
        items = find_item(current_directory, arguments[0])
        for item in items:
            print(item.name)

    elif command_name == "grep":
        matches = grep_pattern(current_directory, arguments[0])
        # files = grep_pattern(current_directory, arguments[0])
        for file_name, line_number, line in matches:
            print(f"{file_name}:{line_number}: {line}")
            
    elif command_name == "wc":
        file = find_file_in_directory(current_directory, arguments[0])
        if file:
            lines, words, chars = wc_file(file)
            print(f"{file.name}:")
            print(f"Lines: {lines}")
            print(f"Words: {words}")
            print(f"Characters: {chars}")

    elif command_name == "file":
        item = find_file_or_directory_in_directory(current_directory, arguments[0])
        if item:
            print(f"{arguments[0]}: {file_type(item)}")

    elif command_name == "zip":
        zip_directory(current_directory, arguments[0])

    elif command_name == "unzip":
        unzip_to_directory(arguments[0], current_directory)
    elif command_name == "help":
        print("Available commands:")
        for cmd, description in COMMANDS.items():
            print(f"{cmd}: {description}")
        return
                    

def clear_screen():
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Unix-based (Linux, macOS, etc.)
        os.system("clear")

def run_virtual_system():
    fs = FileSystem()
    print("You've entered the Virtual System.")
    while True:
        command = input(f"\nshiril@shiril\n  > ")
        if not command: 
            continue
        if command == "exit":
            print("Exiting the file system...")
            break
        execute_command(command, fs)

