import os
import shutil
import subprocess
import zipfile

def local_execute_command(command):
    parts = command.split()
    cmd = parts[0]

    if cmd == "ls":
        print("\n".join(os.listdir()))
    elif cmd == "cd":
        path = " ".join(parts[1:])
        try:
            os.chdir(path)
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "mkdir":
        dir_name = " ".join(parts[1:])
        try:
            os.mkdir(dir_name)
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "rmdir":
        dir_name = " ".join(parts[1:])
        try:
            shutil.rmtree(dir_name)
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "touch":
        file_name = " ".join(parts[1:])
        try:
            with open(file_name, 'w') as f:
                pass
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "rm":
        file_name = " ".join(parts[1:])
        try:
            os.remove(file_name)
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "cat":
        file_name = " ".join(parts[1:])
        try:
            with open(file_name, 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"Error: {e}")

    elif cmd == "pwd":
        print(os.getcwd())
    elif cmd == "cp":
        src, dest = parts[1], parts[2]
        try:
            shutil.copy(src, dest)
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "mv":
        src, dest = parts[1], parts[2]
        try:
            shutil.move(src, dest)
        except Exception as e:
            print(f"Error: {e}")

    elif cmd == "grep":
        pattern, file_name = parts[1], parts[2]
        try:
            with open(file_name, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if pattern in line:
                        print(line.strip())
        except Exception as e:
            print(f"Error: {e}")
        
    elif cmd == "append":
        file_name = parts[1]
        try:
            with open(file_name, 'a') as f:
                print(f"Appending to {file_name}. Enter your content (type 'EOF' on a new line to stop):")
                while True:
                    line = input()
                    if line == 'EOF':
                        break
                    f.write(line + "\n")
            print(f"Content appended to {file_name}")
        except Exception as e:
            print(f"Error: {e}")

    elif cmd == "edit":
        file_name = parts[1]
        print(f"Editing '{file_name}'. Enter new content (type 'EOF' on a new line to end):")
        lines = []
        while True:
            line = input()
            if line == "EOF":
                break
            lines.append(line)
        try:
            with open(file_name, 'w') as f:
                f.write("\n".join(lines))
            print(f"Saved changes to '{file_name}'.")
        except Exception as e:
            print(f"Error: {e}")
    elif cmd == "clear":
        # Check the operating system
        if os.name == "posix":  # Unix/Linux/MacOS/BSD/etc.
            os.system("clear")
        elif os.name in ("nt", "dos", "ce"):  # Windows
            os.system("cls")

    elif cmd == "help":
        help_messages = {
            "ls": "List directory contents. Usage: ls",
            "mkdir": "Create a directory. Usage: mkdir [directory_name]",
            "touch": "Create a file. Usage: touch [file_name]",
            "rm": "Remove a file. Usage: rm [file_name]",
            "rmdir": "Remove a directory. Usage: rmdir [directory_name]",
            "cat": "Display file contents. Usage: cat [file_name]",
            # "chmod": "Change file permissions. Usage: chmod [mode] [file_name]",
            "cd": "Change directory. Usage: cd [path]",
            "pwd": "Print working directory.",
            "cp": "Copy a file. Usage: cp [source] [destination]",
            "mv": "Move a file. Usage: mv [source] [destination]",
            # "find": "Find files by name. Usage: find [path] [pattern]",
            "grep": "Search for a pattern in a file. Usage: grep [pattern] [file_name]",
            # "zip": "Compress files into a zip archive. Usage: zip [archive_name] [file1] [file2] ...",
            # "unzip": "Extract files from a zip archive. Usage: unzip [archive_name]",
            "append": "Append text to a file. Usage: append [file_name] [text]",
            "edit": "Edit a file's content. Usage: edit [file_name]",
            "clear": "Clear the terminal",
            "exit": "Exit the system."
        }
        for command, description in help_messages.items():
            print(f"{command}: {description}")
    else:
        print(f"Command '{command}' not recognized, use 'help' to see all commands")

def run_local_system():
    print("You've chosen the Local System.")
    while True:
        command = input(f"\n{os.getcwd()}> ")
        if not command: 
            continue
        if command == "exit":
            print("Exiting the file system...")
            break
        local_execute_command(command)
